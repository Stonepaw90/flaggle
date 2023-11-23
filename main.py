import streamlit as st
import pandas as pd
import random as rand
import os

# import os
# os.system(r"cd /D C:\Users\Abraham\miniconda3\envs\snowflakes\Scripts | streamlit run main.py")
# os.system("streamlit run main.py")
st.set_page_config(page_title="Flaggle")  # , page_icon=":world_map:")
st.markdown("### Coded by [Abraham Holleran](https://github.com/Stonepaw90) :sunglasses:")
st.write("From just the outline and flag below, can you guess the country in six guesses?")
st.write("Enter the first six letters of the country name. Note that a 🟨 tells you the letter is used somewhere in the whole country name, not just in the first six letters.")

class flaggle:
    def __init__(self):
        flags_csv = pd.read_csv("flags_iso2.csv")
        flags_csv = flags_csv.rename(columns={"Alpha-3 code": "iso", "Alpha-2 code": "iso2"})
        flags_csv = flags_csv.drop(flags_csv.loc[flags_csv["iso2"] == "mh"].index)
        flags_csv = flags_csv.drop(flags_csv.loc[flags_csv["iso2"] == "ps"].index)
        flags_csv = flags_csv.drop(flags_csv.loc[flags_csv["iso2"] == "tv"].index)
        flags_csv = flags_csv.drop(flags_csv.loc[flags_csv["iso2"] == "fm"].index)
        flags_csv = flags_csv.reset_index(drop=True)
        # flags_csv = flags_csv[flags_csv["iso2"] not in no_images] #so these do have images
        flags_csv["URL"] = list(map(lambda s: s.replace("small/tn_", ""), flags_csv["URL"]))
        self.flags_csv = flags_csv
        self.iso2 = self.flags_csv["iso2"]
        self.countries = list(map(str.lower, self.flags_csv["Country"]))
        self.countries_capitalized = self.flags_csv["Country"].to_list()
        self.countries_padded = [(i + "      ")[:6] for i in self.countries]
        self.url = self.flags_csv["URL"]
        self.flags_csv_len = len(self.flags_csv)
        self.flags_dict = {self.iso2[i]:
                               {"country_name": self.countries[i],
                                "country_name_capital": self.countries_capitalized[i],
                                "flag_url": self.url[i],
                                "padded": self.countries_padded[i]}
                           for i in range(self.flags_csv_len)}
        self.tries = 0

    def choose_country(self):
        self.secret_flag_index = rand.randrange(self.flags_csv_len)
        self.secret_country = self.iso2[self.secret_flag_index]
        self.country_dict = self.flags_dict[self.secret_country]
        self.country_capitalized = self.country_dict["country_name_capital"]
        self.secret_padded = self.country_dict["padded"]
        self.COUNTRY_TEXT = self.country_dict['country_name']
        self.country_len = len(self.COUNTRY_TEXT)

    def display_sidebar(self):
        st.sidebar.header("For hard mode, close the sidebar!")
        st.sidebar.subheader("Country list:")
        for i in self.flags_csv["Country"].to_list():
            st.sidebar.write(i)

    def print_flag_and_png(self):
        col = st.columns(2)
        col[1].image(self.country_dict['flag_url'], use_column_width=True, caption="Country flag")
        col[0].image(f"https://raw.githubusercontent.com/Stonepaw90/flaggle/main/all-512/{self.secret_country}/512.png",
                     use_column_width=True, caption="Country Outline")

    def print_blanks(self):
        blank_text = ['_'] * self.country_len
        for i in range(self.country_len):
            if self.COUNTRY_TEXT[i] == " ":
                blank_text[i] = ' '
        return ''.join(blank_text)
        #st.title("The country name is " + self.blank_text + ".")

    def initialize_flaggle(self):
        st.session_state['flaggle'] = self
        self.count = 1

    def get_guess(self):
        ordinal = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', "seventh", "eighth", "ninth", "tenth"]
        if 'guest_list' not in st.session_state:
            st.session_state.guess_list = [''] * 10
        # st.write(f"count = {self.count}")
        for i in range(min(self.count, 6)):
            st.session_state.guess_list[i] = st.text_input(f"What is your {ordinal[i]} guess?",
                                                           placeholder="______", #self.blank_text,
                                                           max_chars=6,
                                                           help = "You can pad your answer with spaces. 'italy ', 'italy', and 'ITALY' are all valid.").lower() #self.country_len
            if st.session_state.guess_list[i]:
                self.to_print = ""
                for idx, letter in enumerate(st.session_state.guess_list[i]):
                    if st.session_state.guess_list[i][idx] == self.secret_padded[idx]:
                        self.to_print += "🟩"
                    elif st.session_state.guess_list[i][idx] in self.COUNTRY_TEXT:
                        self.to_print += "🟨"
                    else:
                        self.to_print += ":black_large_square:"
                st.markdown(self.to_print)
                if self.to_print == "🟩" * 6 or self.to_print == "🟩" * self.country_len:
                    # self.to_print = ""
                    st.balloons()
                    st.title("You did it!!!")
                    return self
        if self.count > 6:
            try:
                st.title(f"The answer was {self.country_capitalized}.")
            except:
                pass
            st.title("Better luck next time!")
            return self
        self.count += 1
        return self


def main():
    flaggle_game = flaggle()
    flaggle_game.choose_country()
    flaggle_game.display_sidebar()
    if 'flaggle' not in st.session_state:
        flaggle_game.initialize_flaggle()
        st.rerun()  # now this loop will not be hit again
    flaggle_game = st.session_state['flaggle']
    flaggle_game.print_flag_and_png()
    with st.expander("Need a hint? Click here."):
        st.write("The country name looks like '" + flaggle_game.print_blanks() + "'")
    st.session_state['flaggle'] = flaggle_game.get_guess()
    if st.button("Try again with different flag"):
        del st.session_state['flaggle']
        del st.session_state.guess_list
        st.write(st.session_state)
        st.rerun()


main()
