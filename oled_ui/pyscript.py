from pynput.keyboard import Key, Listener
print('hello world')

def on_key_release(key):
    if key == Key.up:
        print('up pressed')
    if key == Key.down:
        print('down pressed')
    if key == Key.right:
        print('right pressed')
    if key == Key.left:
        print('left pressed');

with Listener(on_release = on_key_release) as listener:
    listener.join()