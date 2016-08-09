import pyglet

from random import randint

hello_sounds = ['activated.wav', 'hello.wav', 'sentry mode activated.wav', 'i dont hate you.wav', 'hey its me.wav']

found_sounds = ['there you are.wav', 'there you are.wav(2)', 'who\'s there.wav', 'gotcha.wav']

shooting_sounds = ['who\'s there.wav', 'dispensing product.wav', 'i dont hate you.wav']

lost_sounds = ['is anyone there.wav', 'target lost.wav', 'sleep mode activated.wav']


random_sound = randint(0, 4)

sound = pyglet.media.load('data/' + hello_sounds[random_sound], streaming=False)
sound.play()
pyglet.app.run()

pyglet.app.exit()