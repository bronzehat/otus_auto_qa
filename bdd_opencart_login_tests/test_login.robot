*** Settings ***
Documentation    Test suite for test login as admin and customer in OpenCart
Library          SeleniumLibrary     implicit_wait=5.0
Library          Login.py
*** Test Cases ***
Admin Login
    Login Admin

User Login
    Login User

