*** Settings ***
Documentation       Simple Opencart tests using SeleniumLibrary.
Library             SeleniumLibrary     timeout=5.0    implicit_wait=5.0    screenshot_root_directory=screens/
Library             String
Library             Collections
Suite Setup         Run Keywords    Log In      Open Products Page
Suite Teardown      Run Keywords    Log Out     Close All Browsers


*** Variables ***
${LOGIN URL}        http://192.168.85.154/opencart/admin/
${BROWSER}          Firefox
${LOGIN}            root
${PASSWORD}         o9p0[-]=
${SUCCESS_ALERT}    Success
${PRODUCT_NAME}     TestProduct
${PRODUCT_TITLE}    TestProductTitle
${PRODUCT_MODEL}    TestProductModel
${PRODUCT_KEYWORD}  TestKeyword

*** Test Cases ***
Test Add Product
    Given decided to add new product
    And entered product name and product title
    And entered product model
    When saved changes
    Then success alert is on page

Test Edit Product
    Given found product     ${PRODUCT_NAME}
    And opened product edit page
    And filled product keyword  ${PRODUCT_KEYWORD}
    When saved changes
    Then success alert is on page

Test Delete Product
    Given found product     ${PRODUCT_NAME}
    And chosen product
    When pushed product delete button
    Then success alert is on page

*** Keywords ***
Log In
    Open Browser        ${LOGIN URL}    ${BROWSER}
    Input Username      ${LOGIN}
    Input Password      ${PASSWORD}
    Click Button        Login

Log Out
    Click Element       xpath://a[contains(@href, 'route=common')]

Input Username
    [Arguments]     ${username}
    Input Text      username    ${username}

Input Password
    [Arguments]     ${password}
    Input Text      password    ${password}

Open Products Page
    Click Element   partial link:Catalog
    Click Element   partial link:Products

decided to add new product
    Click Element   xpath://a[contains(@data-original-title,'Add New')]

entered product name and product title
    Input Text      id:input-name1   ${product_name}
    Input Text      id:input-meta-title1    ${product_title}

entered product model
    Click Link      Data
    Input Text      name:model   ${product_model}

saved changes
    Click Element   xpath://button[@data-original-title='Save']

success alert is on page
    Page Should Contain     ${SUCCESS_ALERT}

found product
    [Arguments]     ${product_name}
    Input text      xpath://input[@placeholder="Product Name"]      ${product_name}
    Click Button    Filter

opened product edit page
    Click Element   xpath://a[contains(@data-original-title,'Edit')]

filled product keyword
    [Arguments]     ${product_keyword}
    Input text      id:input-meta-keyword1      ${product_keyword}

chosen product
    Click Element   name:selected[]

pushed product delete button
    Click Element   xpath://button[contains(@formaction, 'route=catalog/product/delete')]
    Handle Alert    timeout=5