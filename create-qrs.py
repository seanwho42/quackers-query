import csv
import qrcode
from PIL import Image
from PIL import ImageDraw

# todo update this when we implement a domain name
# todo set this up with proper ids and make it in a more printable format -- using PIL?
def generate_qr_code(duck_id):
    url = f'http://137.184.35.65:81/form?duck_id={duck_id}'  # todo update
    qr = qrcode.QRCode(version=1, box_size=3, border=15)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# img.save(f"./qr_codes/qr_code_{duck_id}.png")

file = open('duck_db_seed.csv')
ducks = csv.reader(file)
duck_rows = 0
template_qr = generate_qr_code('0Eaton1stHigh1')

for row in ducks:
    duck_rows += 1
    print(duck_rows)
print(duck_rows)


def concatenate_qr_codes(duck_data, n_cols):
    # making it a function in case we want to use qr codes for data entry as well...
    # template_img = generate_qr_code(data[0][5])
    # width = template_img.width
    # height = template_img.height
    n = 0
    n_rows = 180
    temp_qr = generate_qr_code('test_string')
    temp_qr.save('template_qr_code_for_jank.png')
    temp_img = Image.open('template_qr_code_for_jank.png')
    print(f"temp_img.width = {temp_img.width}")
    canvas = Image.new('RGB', (temp_img.width*n_cols, temp_img.height*(n_rows//n_cols))) #temporarily just made it real big

    for duck in duck_data:
        row = n // n_cols
        col = n % n_cols
        # save the qr code image
        id = duck[5]
        qr_img = generate_qr_code(id)
        qr_img.save(f"./qr_codes/qr_code_{id}.png")
        print(f'col={col} row={row}')

        # read the duck qr image because I guess the width of a qr code image isn't the right thing
        # probably would be better if using the qrcode with the pil dependency?
        reread_qr = Image.open(f"./qr_codes/qr_code_{id}.png")
        x = col*reread_qr.width
        y = row*reread_qr.height
        canvas.paste(reread_qr, (x, y))
        editable = ImageDraw.Draw(canvas)
        editable.text((x+45, y+30), text=str(id), fill=(0, 0, 0))
        n += 1
    canvas.save(f"qr_sheet.png")


if __name__ == '__main__':
    concatenate_qr_codes(duck_data=csv.reader(open('duck_db_seed.csv')), n_cols=5)
