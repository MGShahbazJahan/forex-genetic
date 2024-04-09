import streamlit as st
import requests 


def main():
    response = requests.get('http://127.0.0.1:8000')


if __name__ == "__main__":
    main()