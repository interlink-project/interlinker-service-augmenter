formio = {
    "name": "Example name",
    "formSchema": {
        "components": [
            {
                "key": "age",
                "label": "age-text",
                "type": "textfield",
                "validate": {
                    "required": True
                }
            },
            {
                "key": "submit",
                "label": "submit-text",
                "type": "button"
            },
        ],
    },
    "translations": {
        "language": "en",
        "i18n": {
            "en": {
                "submit-text": "Submit",
                "age-text": "Age"
            },
            "es": {
                "submit-text": "Enviar",
                "age-text": "Edad"
            }
        },
    },
    "type": "default"
}
