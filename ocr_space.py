import requests


class OcrSpace:
    def __init__(self, api_key):
        self.api_key = api_key

    def ocr_space_file(self, filename, overlay=False, language='eng'):
        """ OCR.space API request with local file.
        :param filename: Your file path & name.
        :param overlay: Is OCR.space overlay required in your response.
                        Defaults to False.
        :param language: Language code to be used in OCR.
                        Defaults to 'en'.
        :return: Result in JSON format.
        """
        payload = {'isOverlayRequired': overlay,
                   'apikey': self.api_key,
                   'language': language,
                   'OCREngine': 2

                   }
        with open(filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={filename: f},
                              data=payload, timeout=5000
                              )

        return r.content.decode()

    def ocr_space_url(self, url, overlay=False, language='eng'):
        """ OCR.space API request with remote file.
        :param url: Image url.
        :param overlay: Is OCR.space overlay required in your response.
                        Defaults to False.
        :param api_key: OCR.space API key.
                        Defaults to 'helloworld'.
        :param language: Language code to be used in OCR.
                        Defaults to 'en'.
        :return: Result in JSON format.
        """

        payload = {'url': url,
                   'isOverlayRequired': overlay,
                   'apikey': self.api_key,
                   'language': language,
                   'OCREngine': 2
                   }
        r = requests.post('https://api.ocr.space/parse/image',
                          data=payload
                          )
        return r.content.decode()
