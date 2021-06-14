from wiki_extractor import create_wiki_list
from .text_transformation_base import TextTransformationBase
from loguru import logger


class NETransformation(TextTransformationBase):
    def spacy_replace(self, txt: str, **kwargs) -> str:
        logger.info(f'transform "{txt}" with args {str(kwargs)}')
        ne_texts = kwargs['ne_texts']
        ne_types = kwargs['ne_types']
        idx = 0
        for i, ne_text in enumerate(ne_texts):
            new_text = "<'" + ne_text + "', " + ne_types[i] + ">"
            f_idx = txt[idx:].find(ne_text)
            f_idx += idx
            if f_idx >= idx:
                txt = txt[:f_idx] + new_text + txt[f_idx+len(ne_text):]
                idx = f_idx + len(ne_text)
        return txt

    def apply(self, txt: str, **kwargs) -> str:
        logger.info(f'transform "{txt} with args {str(kwargs)}')
        for m in self.mountains:
            # The NE cannot be part of another token, therefore check for
            # leading and trailing separators
            s = f' {m} '
            txt = txt.replace(s, ' mountain ')
            s = f' {m},'
            txt = txt.replace(s, ' mountain,')
            s = f' {m}.'
            txt = txt.replace(s, ' mountain.')
            if txt.startswith(m + ' '):
                txt = 'Mountain' + txt[len(m):]
        return txt

    def __init__(self):
        super().__init__("NamedEntities")
        self.mountains = create_wiki_list('https://en.wikipedia.org/wiki/Special:Export/List_of_mountains_by_elevation')
