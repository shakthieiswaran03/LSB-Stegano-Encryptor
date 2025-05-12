from PIL import Image

def _int_to_bin(rgb):
    return tuple(format(i, '08b') for i in rgb)

def _bin_to_int(rgb_bin):
    return tuple(int(b, 2) for b in rgb_bin)

def encode_image(input_path, output_path, secret_text):
    img = Image.open(input_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    binary_text = ''.join(format(ord(i), '08b') for i in secret_text) + '1111111111111110'
    img_data = img.getdata()
    new_data = []

    data_index = 0
    for pixel in img_data:
        if data_index < len(binary_text):
            r, g, b = _int_to_bin(pixel)
            r = r[:-1] + binary_text[data_index] if data_index < len(binary_text) else r
            data_index += 1
            g = g[:-1] + binary_text[data_index] if data_index < len(binary_text) else g
            data_index += 1
            b = b[:-1] + binary_text[data_index] if data_index < len(binary_text) else b
            data_index += 1
            new_pixel = _bin_to_int((r, g, b))
            new_data.append(new_pixel)
        else:
            new_data.append(pixel)

    encoded_img = Image.new(img.mode, img.size)
    encoded_img.putdata(new_data)
    encoded_img.save(output_path, format='PNG')
    print(" Encoding complete.")

def decode_image(image_path):
    img = Image.open(image_path)
    binary_data = ""
    for pixel in img.getdata():
        for color in pixel:
            binary_data += format(color, '08b')[-1]

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_text = ""
    for byte in all_bytes:
        if byte == '11111110': 
            break
        decoded_text += chr(int(byte, 2))
    return decoded_text
