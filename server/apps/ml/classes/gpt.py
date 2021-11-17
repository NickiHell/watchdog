import random

from transformers import GPT2LMHeadModel, GPT2Tokenizer


class SmallGPT3:
    def __init__(self, model_name: str, params: dict = None):
        self._model_name: str = model_name
        self._model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained(self._model_name)
        self._tokinizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained(self._model_name)
        self._memory = []
        self._params: dict = params or {
            'top_k': 5,
            'top_p': 0.95,
            'temperature': 0.85,
            'repetition_penalty': 3.0,
            'max_length': 128,
            'num_beams': 3,
            'do_sample': True,
            'no_repeat_ngram_size': 3,
            'pad_token_id': self._tokinizer.encode('.')[0],
            'length_penalty': 0.95,
            'num_return_sequences': random.randint(1, 5),
        }

    def _generate(self, text: str) -> str:
        input_ids = self._tokinizer.encode(text, return_tensors="pt")
        out = self._model.generate(
            input_ids,
            **self._params,
        )
        return [self._tokinizer.decode(x) for x in out][0]

    @staticmethod
    def _text_post_processing(message: str, text: str) -> str:
        # text: str = text.replace(message, '')
        text: str = ' '.join(text.split()).strip().capitalize()
        return text

    def __call__(self, *args, **kwargs):
        message: str = args[0]
        output: str = self._text_post_processing(message, self._generate(message))
        return output
