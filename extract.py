from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster

class Photo:

    def __init__(self):
        # Determines top 10 colors
        self.NUM_CLUSTERS = 10

        # Load the image
        self.im = None

        # Get the total number of pixels
        self.num_pixels = None

        # Sort the clusters by count and get the top 10
        self.sorted_clusters = None

        self.color_dict = None
    def open_image_from_server(self,image_source):


        # Load the image
        im = Image.open(image_source)

        #Resize the image to reduce load time
        self.im = im.resize((50,50))

        # Get the total number of pixels
        self.num_pixels = self.im.size[0] * self.im.size[1]

        #Convert image to RGB
        im_rgb = self.im.convert('RGB')

        # Convert the image to a numpy array
        ar = np.asarray(im_rgb)

        # Reshape the array to a 2D array of pixels and 3 color values (RGB)
        shape = ar.shape
        ar = ar.reshape(np.prod(shape[:2]), shape[2]).astype(float)

        # Find the clusters using k-means clustering
        codes, dist = scipy.cluster.vq.kmeans(ar, self.NUM_CLUSTERS)

        # Assign each pixel to a cluster
        vecs, dist = scipy.cluster.vq.vq(ar, codes)

        # Count the occurrences of each cluster
        counts, bins = np.histogram(vecs, len(codes))

        # Sort the clusters by count and get the top 10
        self.sorted_clusters = sorted(zip(codes, counts), key=lambda x: x[1], reverse=True)[:10]

    def rgb_to_hex(self, r, g, b):
        hex_value ='#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b))
        return hex_value

    # Print the top 10 clusters
    def show_top_10(self):
        for i, (color, count) in enumerate(self.sorted_clusters):
            self.rgb_to_hex(color[0], color[1], color[2])

        self.color_dict = {
            f'Color {i + 1}': {'RGB': color, 'Percentage': round(count/self.num_pixels*100,2)} for
            i, (color, count) in enumerate(self.sorted_clusters)}

        for i, (color, count) in enumerate(self.sorted_clusters):
            hex_value = self.rgb_to_hex(color[0], color[1], color[2])
            self.color_dict[f'Color {i + 1}']['Hex'] = hex_value
