*** Settings ***
Documentation       Simple Opencart tests using SeleniumLibrary.
Library             SeleniumLibrary     timeout=5.0    implicit_wait=5.0    screenshot_root_directory=screens/
Library             String
Library             Collections
Suite Setup         Open OpenCart Page
Suite Teardown      Close All Browsers


*** Variables ***
${URL}              http://192.168.85.154/opencart
${BROWSER}          Firefox
${SUCCESS_ALERT}    Success
${EMPTY_CART_ALERT}     Your shopping cart is empty
${PRODUCT_PARENT_CATEGORY}  Desktops
${PRODUCT_CATEGORY}  Mac
${PRODUCT_NAME}  iMac
${PRODUCT_QUANTITY}     10
${CURRENCY}     USD

*** Test Cases ***
Test Add Product To Cart
    Given chosen product category      ${PRODUCT_PARENT_CATEGORY}    ${PRODUCT_CATEGORY}
    And opened product page     ${PRODUCT_NAME}
    When added product to cart
    Then success alert is on page

Test Edit Product In Cart Quantity
    Given opened cart
    When edit product quantity      ${PRODUCT_QUANTITY}
    Then success alert is on page

Test Delete Product From Cart
    Given opened cart
    When deleted product from cart
    Then empty cart alert is on page

Test Change Currency
    Given opened currencies list
    When chosen currency        ${CURRENCY}
    Then site currency is correct

Test Site Owner Info
    When owner info page is open
    Then get site owner info

*** Keywords ***
Open OpenCart Page
    Open Browser        ${URL}    ${BROWSER}

chosen product category
    [Arguments]  ${parent_category}      ${product_category}
    Click Element       partial link:${parent_category}
    Click Element       partial link:${product_category}

opened product page
    [Arguments]  ${product_name}
    Click Link   ${product_name}

added product to cart
    Click Button       Add to Cart

success alert is on page
    Page Should Contain     ${SUCCESS_ALERT}

opened cart
    Click Element       xpath://a[@title='Shopping Cart']

edit product quantity
    [Arguments]     ${product_quantity}
    Input Text      xpath://input[contains(@name, 'quantity')]    ${product_quantity}
    Click Element   xpath://button[@data-original-title='Update']

deleted product from cart
    Click Element   xpath://button[@data-original-title='Remove']

empty cart alert is on page
    Page Should Contain     ${EMPTY_CART_ALERT}

opened currencies list
    Click Element       css:form#form-currency

chosen currency
    [Arguments]     ${currency}
    Click Button   name:${currency}

site currency is correct
    ${currency_mark}    Get Text     css:button strong
    log to console      ${\n}${currency_mark}
    should contain      ${currency_mark}    $

owner info page is open
    Click Link      About Us

get site owner info
    ${site_owner_info}      Get Text    css:div#content p
    log to console          ${\n}${site_owner_info}