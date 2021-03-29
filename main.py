from package.src.file_processor import FileProcessor

x = FileProcessor.load_csv("data/input.csv")
for item in x:
    print(item.display_str())
