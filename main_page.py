from PIL import Image
from additional import *

st.set_page_config(page_title="Fourier transform filters", page_icon="🎨",layout="wide",
                    menu_items={"About":"This app is created in 2024 as a part of bachelor degree qualification project in compuer sciense"})


st.header("**Fourier transform frequency filters**")

with open("tips.txt", 'r') as f:
    st.sidebar.markdown(f.read())

image_file = st.file_uploader("Choose an image to start:", 
                    type=["png", "jpg", "jpeg"], 
                    on_change=img_changed,
                    help="Everything you've done previously " \
                    "is cleared each time you upload new file")

if image_file is not None:

    st.write("Original image:")
    st.image(image_file)
    st.divider()

    left1, right1 = st.columns(2)

    with left1:

        st.write("Grayscale:")
        img = Image.open(image_file).convert('L')
        st.image(img)

        image_bytes = img_to_bytes(img)
        st.download_button("Download grayscale image", image_bytes,
                                    file_name="grayscale_"+image_file.name, mime="image/png")
        image = crop_to_even_shape(np.array(img))

    with right1:

        if st.session_state["new"]:
            st.button('Apply Fourier Transform', on_click=apply_transform, args=(image,True))
        
        else:
            st.write("Magnitude spectrum:")
            spectrum = ft.spectrum(st.session_state["original_ft"])
            spectrum_image = Image.fromarray(spectrum).convert('L')
            st.image(spectrum_image)

            spectrum_bytes = img_to_bytes(spectrum_image)
            st.download_button("Download spectrum image", spectrum_bytes,
                file_name="spectr_"+image_file.name, mime="image/png")

    if st.session_state["original_ft"] is not None:

        st.divider()
        st.header("Set filter:")
        filter_option = st.radio( "Choose which filter you need:",
                        ["Low pass", "High pass", "Bond stop", "Bond pass"],
                        captions = ["Change frequencies higher then set value", 
                                    "Change frequencies lower then set value", 
                                    "Change frequencies between set values",
                                    "Change frequencies apart from those between set values"])

        _min, _max, _average = d_values(st.session_state["original_ft"])

        if filter_option == "High pass" or filter_option == "Low pass":
            d0 = st.number_input("Set cut-off d value:",_min, _max, _average,
                        help=f"Distance from spectrum center. Max value you can set is {_max} and min value is {_min}")
            d1 = None
        
        if filter_option == "Bond stop" or filter_option == "Bond pass" :
            d0 = st.number_input("Set lower d value:",_min, _max, _average*0.8,
                        help=f"Distance from spectrum center. Max value you can set is {_max} and min value is {_min}")
            d1 = st.number_input("Set higher d value:",_min, _max, _average*1.2)

        coef = st.slider("Choose the coeficient to multiply with frequencies:",0.0,3.0,1.0,0.05,
                                help="Value 1 here leaves all frequencies the same")

        st.button("Apply filter",on_click=apply_filter,args=(filter_option,d0, d1, coef))

        if st.session_state["filtered_ft"] is not None:

            st.divider()
            left2, right2 = st.columns(2)

            with left2:

                st.write("Magnitude spectrum after filtering:")
                spectrum_filtered = ft.spectrum(st.session_state["filtered_ft"])
                spectrum_filtered_image = Image.fromarray(spectrum_filtered).convert('L')
                st.image(spectrum_filtered_image)

                filtered_spectrum_bytes = img_to_bytes(spectrum_filtered_image)
                st.download_button("Download filtered spectrum image", filtered_spectrum_bytes,
                                    file_name="filtered_spectr_"+image_file.name, mime="image/png")
            with right2:

                st.write("Image after reverse transform:")
                transform_filtered = ft.reverse_ft_shift(st.session_state["filtered_ft"])
                image_filtered = ft.reverse_fft2(transform_filtered)
                img_result = np.abs(image_filtered)

                image_result = Image.fromarray(img_result).convert('L')
                st.image(image_result)

                image_result_bytes = img_to_bytes(image_result)
                st.download_button("Download filtered image", image_result_bytes,
                                    file_name="filtered_"+image_file.name, mime="image/png")

st.divider()

# приклади
if "examples_shown" not in st.session_state:
    st.session_state["examples_shown"] = False
    st.button("Show examples", on_click=show_examples)
else:
    if not st.session_state["examples_shown"]:
        st.button("Show examples", on_click=show_examples)
    else:
        st.button("Hide examples", on_click=hide_examples)
        st.write("Here are some examples. All filters are applied to same image so that the difference was more obvious.")
        for example in examples_dicts:
            st.write(example["Descryption"])
            left, right = st. columns(2)
            with left:
                st.image(example["Spectrum"])
            with right:
                st.image(example["Image"])
        st.button("Hide this examples", on_click=hide_examples)
