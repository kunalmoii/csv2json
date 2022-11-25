from imports_lib import *
from settings import __APP_SETTINGS__


# print("--Reading CSV--")
data = pd.read_csv(f'csv_file/{__APP_SETTINGS__.CSV_PATH}')

# creating dictionary
json_data = {'categories': [], 'images': [], 'annotations': []}

# classes
classes = __APP_SETTINGS__.CLASS_NAMES

for index, category in enumerate(classes):
    out = {"id": index, "name": category}
    json_data['categories'].append(out)

print()
print(json_data['categories'])
print()

temp_image_id = 0
image_id = 0
for info in range(len(data['labels'])):

    try:
        image_info = ast.literal_eval(data['labels'][info])
    except:
        pass
    file_name = data['image'][info]
    try:
        try:
            image_width = image_info[0]['original_width']
            image_height = image_info[0]['original_height']
        except:
            image_width = image_info[1]['original_width']
            image_height = image_info[1]['original_height']
    except:
        pass

    # to save filename with bucket url eg: "gs://input-bucket-2e42ed/frame_1137.jpg"
    json_data['images'].append({'file_name': file_name,
                                'height': image_height,
                                'width': image_width,
                                'id': image_id})

    # to save filename with actual frame name eg: "frame_1137.jpg"
    # json_data['images'].append({'file_name': file_name.split('/')[-1],
    #                         'height': image_height,
    #                         'width': image_width,
    #                         'id': image_id})

    image_info_labels = len(image_info)
    for anno in range(image_info_labels):
        try:
            x_min = image_info[anno]['x']
            y_min = image_info[anno]['y']
            x_max = image_info[anno]['width']
            y_max = image_info[anno]['height']
            labels = image_info[anno]['labels'][0]

            for id, categories in enumerate(classes):
                if labels == categories:
                    category_id = id

            json_data['annotations'].append({'area': int(x_max)*int(y_max),
                                             'iscrowd': 0,
                                             'image_id': image_id,
                                             'bbox': [int((x_min/100)*image_width), int((y_min/100)*image_height), int((x_max/100)*image_width), int((y_max/100)*image_height)],
                                             'category_id': category_id,
                                             'id': temp_image_id,
                                             'ignore': 0,
                                             'segmentation': []})

            temp_image_id = temp_image_id+1
        except:
            pass

    image_id = image_id+1


with open(f"output_json/{__APP_SETTINGS__.OUTPUT_JSON}", "w") as outfile:
    json.dump(json_data, outfile, indent=1)

print("JSON GENERATED SUCCESSFULLY")
