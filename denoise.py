import cv2


def denoise(input_path, h=10, template_window_size=7, search_window_size=21):
    img = cv2.imread(input_path)
    denoised = cv2.fastNlMeansDenoisingColored(img, None, h, h, template_window_size, search_window_size)
    cv2.imwrite(input_path, denoised)
