The following is the structure of the code.

1. sim1.py file runs with the argument for number of users and number of sniffers and generates 2 files: sniffed_user.json(data received by the sniffers) and user_data.json(ground truth of every user)

2. Next, we run tracking.py to find the linkability between the identifiers. Here, 2 files are created, manager.pkl which consists of the information of devices with their corresponding identifiers(bluetooth,wifi and LTE) and linked_ids.json which maps the linking between randomized identifiers.

3. Next, we check the success of our mapping by running the code sanity_linking.py which gives us the number of mappings that are correctly identified.

4. Next, we run the reconstruction.py to generate the reconstructed path and measure the duration of tracking possible through the mappings.
