import streamlit as st
import pandas as pd
import random as rand
from PIL import Image

# import os
# os.system(r"cd /D C:\Users\Abraham\miniconda3\envs\snowflakes\Scripts | streamlit run main.py")
# os.system("streamlit run main.py")
st.set_page_config(page_title="Flaggle", page_icon=":world_map:")
st.markdown("### Coded by [Abraham Holleran](https://github.com/Stonepaw90) :sunglasses:")


class flaggle:
    def __init__(self):
        flags_csv = pd.read_csv("flags_iso.csv")
        flags_csv = flags_csv.rename(columns={"Alpha-3 code": "iso", "Alpha-2 code": "iso2"})
        flags_csv["URL"] = list(map(lambda s: s.replace("small/tn_", ""), flags_csv["URL"]))
        self.flags_csv = flags_csv
        self.iso2 = self.flags_csv["iso2"]
        self.countries = list(map(str.lower, self.flags_csv["Country"]))
        #self.iso = self.flags_csv["iso"]
        self.url = self.flags_csv["URL"]
        self.flags_csv_len = len(self.flags_csv)
        self.flags_dict = {self.iso2[i]: {"country_name": self.countries[i], "flag_url": self.url[i]} for i in
                           range(self.flags_csv_len)}

    def choose_country(self):
        self.secret_flag_index = rand.randrange(self.flags_csv_len)
        self.secret_country = self.iso2[self.secret_flag_index]
        try:
            #self.png = Image.open(f"\\all-512\\{self.secret_country}\\512.png")
            self.png = Image.open(f"\all-512\512.png")
        except:
            self.choose_country()
        self.country_dict = self.flags_dict[self.secret_country]
        self.COUNTRY_TEXT = self.country_dict['country_name']
        self.country_len = len(self.COUNTRY_TEXT)

    def print_flag_and_png(self):
        col = st.columns(2)
        #col[0].markdown(f"![What country flies this flag?]({self.country_dict['flag_url']})")
        col[1].image(self.country_dict['flag_url'], use_column_width=True, caption = "Country flag")
        col[0].image(self.png, use_column_width=True, caption = "Country Outline")

    def print_blanks(self):
        blank_text = ['_'] * self.country_len
        for i in range(self.country_len):
            if self.COUNTRY_TEXT[i] == " ":
                blank_text[i] = ' '
        self.blank_text = ''.join(blank_text)
        st.title("The country name is " + self.blank_text + ".")

    def initialize_flaggle(self):
        st.session_state['flaggle'] = self
        self.count = 1

    def get_guess(self):
        ordinal = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', "seventh", "eighth", "ninth", "tenth"]
        if 'guest_list' not in st.session_state:
            st.session_state.guess_list = [''] * 10
        # st.write(f"count = {self.count}")
        if self.count > 6:
            st.title("Better luck next time!")
            return self
        for i in range(self.count):
            st.write(self.count)
            # st.write(f"i = {i}")
            # if 'guess_list' in st.session_state:
            # st.write(st.session_state.guess_list)
            # if st.session_state.guess_list[max(i-1, 0)] != '':
            #  st.write(f"Your {ordinal[i-1]} guess was {st.session_state.guess_list[i-1]}")
            st.session_state.guess_list[i] = st.text_input(f"What is your {ordinal[i]} guess?",
                                                           placeholder=self.blank_text,
                                                           max_chars=self.country_len).lower()

            if st.session_state.guess_list[i]:
                to_print = ""
                for idx, letter in enumerate(st.session_state.guess_list[i]):
                    if st.session_state.guess_list[i][idx] == self.COUNTRY_TEXT[idx]:
                        to_print += "🟩"
                    elif st.session_state.guess_list[i][idx] in self.COUNTRY_TEXT:
                        to_print += "🟨"
                    else:
                        to_print += ":black_large_square:"
                st.markdown(to_print)
                if to_print == "🟩" * self.country_len:
                    st.balloons()
                    st.title("You did it!!!")
                    break
        self.count += 1
        return self


def main():
    flaggle_game = flaggle()
    flaggle_game.choose_country()
    if 'flaggle' not in st.session_state:
        flaggle_game.initialize_flaggle()
        st.experimental_rerun()  # now this loop will not be hit again
    flaggle_game = st.session_state['flaggle']
    flaggle_game.print_flag_and_png()
    flaggle_game.print_blanks()
    st.session_state['flaggle'] = flaggle_game.get_guess()
    if st.button("Try again with different flag"):
        del st.session_state['flaggle']
        del st.session_state.guess_list
        st.experimental_rerun()


main()
