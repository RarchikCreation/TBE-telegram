from logics.file.loaded import read_text_file

mentors_info = {
    "karti": [read_text_file("assets/text/1.txt"), ["assets/photo/photo1_1.jpg", "assets/photo/photo1_2.jpg"]],
    "impossible": [read_text_file("assets/text/impossible.txt"), []],
    "mdma": [read_text_file("assets/text/mdma.txt"), ["assets/photo/photo4_1.jpg", "assets/photo/photo4_2.jpg", "assets/photo/photo4_3.jpg"]],
    "sedrick": [read_text_file("assets/text/sedrick.txt"), ["assets/photo/photo5_1.jpg", "assets/photo/photo5_2.jpg", "assets/photo/photo5_3.jpg"]]
}
