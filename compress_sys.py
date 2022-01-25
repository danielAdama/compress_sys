from email.policy import default
import imghdr
import os
from pydoc import doc
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet, ImageSettings, OptimizerSettings

dir = r'/home/daniel/Desktop/programming/pythondatascience/datascience/softwaredev/SRMS'
#key = ## Enter your Demo key here

input_dir = f"{dir}/{'compress_app'}/{'input_pdf'}"
output_dir = f"{dir}/{'compress_app'}/{'output_folder'}"

def scale_byte(byte, factor = 1024):

    """Function to scale byte to it's proper bytes format
    1 byte = 8 bits

    For Example: 1255B / 1024 = 1.23KB, that's to say division goes one step higher in bytes
    and multiplication does otherwise.
    """

    for unit in ['B', 'KB', 'MB', 'GB']:
        if byte < factor:
            return f"{byte:.2f}{unit}"

        byte = byte / factor
    return f"{byte:2f}{unit}"

def compressPDF(dir, input_dir, output_dir, key):
    
    """Function to compress and store the pdf's"""
    files = os.listdir(input_dir)

    for i, file in enumerate(files):
        old_name = f"{file.split('.')[0]}"
        # Reject the file if it's not a pdf document otherwise process.
        if f"{file.split('.')[1]}" != 'pdf':
            print(f"{old_name} is not a PDF document!")
        else:
            new_name = f"{file.split('.')[0]}{i}"
            pdf = f"{input_dir}/{file}"
            initial_scaled = scale_byte(os.path.getsize(pdf))
            initial_size = os.path.getsize(pdf)
            compressed_pdf_path = f"{output_dir}/{new_name}_compressed.pdf"

            # Initialize the compressor framework
            PDFNet.Initialize(key)
            doc = PDFDoc(pdf)
            # Optimize PDF with the default settings
            doc.InitSecurityHandler()
            # Reduce image quality and use jpeg compression for non monochrome images
            image_settings = ImageSettings()
            # low quality jpeg compression
            image_settings.SetCompressionMode(ImageSettings.e_jpeg)
            image_settings.SetQuality(1)
            # Set the output dpi to be standard screen resolution
            image_settings.SetImageDPI(144,96)
            # This option recompress images that was not compressed with the default settings
            image_settings.ForceRecompression(True)
            
            opt_settings = OptimizerSettings()
            opt_settings.SetColorImageSettings(image_settings)
            opt_settings.SetGrayscaleImageSettings(image_settings)
            
            # Use the same settings for both color and grayscale images
            Optimizer.Optimize(doc, opt_settings)
            doc.Save(compressed_pdf_path, SDFDoc.e_linearized)
            doc.Close()

            compressed_scaled = scale_byte(os.path.getsize(compressed_pdf_path))
            compressed_size = os.path.getsize(compressed_pdf_path)

            ratio = 1 - (compressed_size / initial_size)

            print(f"Name of PDF: {old_name}")
            print(f"The Initial size: {initial_scaled}")
            print(f"The Compressed size: {compressed_scaled}")
            print(f"Compression Ratio: {ratio:.2%}")
            print("--"*30)

def main():
    compressPDF(dir, input_dir, output_dir, key)

if __name__ == '__main__':
    main()