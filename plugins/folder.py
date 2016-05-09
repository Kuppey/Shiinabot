import random
import hashlib
import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import utils


def reset_files(move_to, path):
    import shutil
    import time
    for file in os.listdir(move_to):
        src_file = os.path.join(move_to, file)
        dst_file = os.path.join(path, file)
        shutil.move(src_file, dst_file)
    time.sleep(5)


def move_image(image, move_to):
    import shutil
    import time
    time.sleep(10)
    if not os.path.exists(move_to):
        os.makedirs(move_to)
    try:
        shutil.move(image, os.path.join(move_to, ''))
    except:
        # Already in there
        pass


def main(**kwargs):
    file_types = ('.jpg', '.jpeg', '.png', '.gif', '.webm')
    if isinstance(kwargs.get('folder'), list):
        files = []
        for folder in kwargs.get('folder'):
            files += [file for file in os.listdir(folder) if file.endswith(file_types)]
    else:
        files = [file for file in os.listdir(
            kwargs.get('folder')) if file.endswith(file_types)]

    used_images = []
    a_t = kwargs.get('after type')
    if a_t == "move to folder" or a_t == "1":
        move_to = kwargs.get('move folder')
    else:
        try:
            txt_name = kwargs.get('used images')
            used_images = open(
                kwargs.get('used images'), 'r').read().splitlines()
        except:
            txt_name = os.path.join(os.getcwd(),
                                    "Used folder {0}.txt".format(
                                    kwargs['bot name']))
            if not os.path.exists(txt_name):
                print("Didn't find any used links! Creating a TXT!")
                print("Set it to:\n{0}".format(txt_name))
                used_images = []
            else:
                used_images = open(txt_name, 'r').read().splitlines()
    if utils.is_bool(kwargs.get('reset images')) and len(files) < 4 or \
       utils.is_bool(kwargs.get('reset images')) and (
            (len(files) - len(used_images) < 4)):
        if a_t == "text file" or a_t == "2" or a_t is None:
            used_images = used_images[:-4]
        else:
            reset_files(move_to, kwargs.get('folder'))
    try:
        image = random.choice(files)
    except:
        return False, False

    # Fail safe so we don't get stuck in a inf loop
    break_count = 0
    if a_t == "text file" or a_t == "2" or a_t is None:
        write_list = True
        while image in used_images or image is None:
            image = random.choice(files)
            break_count += 1
            if break_count == 50 or not image:
                write_list = False
                break

        if write_list:
            used_images.append(image)
            with open(txt_name, 'w+') as f:
                f.write("\n".join(used_images))
    else:
        from threading import Thread
        Thread(name="Move Image", target=move_image, args=(
            os.path.join(kwargs.get('folder'), image), move_to)).start()

    sn_kwgs = {}
    if "sn" in kwargs.get('message'):
        sn_url, sn_kwgs = utils.saucenao(fname=image[0],
                                         api_key=kwargs.get('saucenao api'),
                                         metainfo=True)
    re_dict = {'(questionmark)': '?',
               '(star)': '*',
               '_': ' '}
    rep = {'{filename clean}': utils.replace_all(
        os.path.splitext(image)[0], re_dict),
           '{filename}': os.path.splitext(os.path.basename(image))[0],
           '{index}': files.index(image),
           '{hash}': hashlib.md5(
                open(os.path.join(
                    kwargs.get('folder'), image), 'rb').read()).hexdigest(),
           '{sn title}': sn_kwgs.get('title'),
           '{sn illust id}': sn_kwgs.get('illust id'),
           '{sn illust url}': sn_url,
           '{sn artist}': sn_kwgs.get('artist'),
           '{sn artist id}': sn_kwgs.get('artist id'),
           '{sn artist url}': sn_kwgs.get('artist url')}
    message = utils.replace_all(kwargs.get('message'), rep)
    image = os.path.join(kwargs.get('folder'), image)
    return(message, image)
