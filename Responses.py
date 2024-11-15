from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    
    if lowered == '':
        return 'Hello?'
    elif lowered == 'hi':
        return 'Hello!'
    elif lowered == 'hello':
        return 'Hi!'
    elif lowered == 'Do you like Declan Rice?':
        return 'I love Declan Rice! hes the best!'
    else:
        return choice([
            'I love Declan Rice!',
            'Declan Rice is the best!',
            'I am a huge fan of Declan Rice!',
            'Declan Rice is my favorite player!',
            'I can talk about Declan Rice all day!',
            'Declan Rice is amazing!',
            'Do you want to know more about Declan Rice?',
            'Declan Rice is a fantastic player!',
            'I admire Declan Rice so much!'
        ])