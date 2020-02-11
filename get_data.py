from controller import Controller
from PIL import Image
from io import BytesIO
from os import listdir
from urllib import request
from time import sleep


def get_data(controller):
    sleep(1)
    try:
        data_source = controller.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/div/main/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div/div'
        )
        data_name = controller.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/div/main/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/div/span'
        )
        data_name = data_name.get_attribute('innerHTML')
        data_url = data_source.value_of_css_property('background-image').split('"')[1]
        rating = input(f'Rating {data_name} [HOT/n]: ')
    except Exception:
        save_data(controller)

    return (data_url, rating)


def save_data(controller):
    url, rating = get_data(controller)
    im_source = request.urlopen(url)

    if rating == '':
        n = last_index('hot') + 1
        f_name = f'data/hot/image_{str(n).zfill(5)}_h.jpg'
        with open(f_name, 'wb') as im:
            im.write(im_source.read())
            im_adjust(f_name)
    else:
        n = last_index('not_hot') + 1
        f_name = f'data/not_hot/image_{str(n).zfill(5)}_nh.jpg'
        with open(f_name, 'wb') as im:
            im.write(im_source.read())
            im_adjust(f_name)

    controller.swipe_left_mobile()
    save_data(controller)


def im_adjust(im):
    with open(im, 'rb') as f:
        io = BytesIO(f.read())

    im_adj = Image.open(io).convert('L')
    im_adj.save(im, quality=5)


def last_index(rating):
    last_n = listdir(f'data/{rating}')
    last_n.sort()
    if last_n == [] or last_n[0] == '.DS_Store':
        last_n = -1
    else:
        last_n = last_n[-1].split('_')[1][-5:]

    return int(last_n)


if __name__ == '__main__':
    controller = Controller()
    controller.login()
    controller.driver.set_window_size(640, 768)  # MacBook 12" halfscreen
    controller.driver.set_window_position(0, 0)
    sleep(5)
    save_data(controller)
