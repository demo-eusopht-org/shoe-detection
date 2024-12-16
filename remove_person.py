import replicate

def remove_person(http_url):
    output = replicate.run(
        "sujaykhandekar/object-removal:153b0087c2576ad30d8cbddb35275b387d1a6bf986bda5499948f843f6460faf",
        input={
            "image_path": http_url,
            "objects_to_remove": "person"
        }
    )
    return output