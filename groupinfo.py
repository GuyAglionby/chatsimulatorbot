import markovify
import ast

class GroupInfo:

    def __init__(self, chat_id, existing_data=None):
        self.chat_id = chat_id
        # If we have a chain saved, then make the model from it
        if existing_data is not None:
            self.model = markovify.Text.from_chain(ast.literal_eval(existing_data))

    def add_message(self, message):
        new_model = markovify.Text(message)

        # If we have a chain saved, then make the model from it
        try:
            self.model = markovify.combine([self.model, new_model])
        except AttributeError:
            self.model = new_model


    def get_data(self):
        return self.model.chain.to_json()
