*** Settings ***
Documentation       Simple Opencart tests using SeleniumLibrary.
Library             SeleniumLibrary     timeout=10.0    implicit_wait=10.0    screenshot_root_directory=screens/
Library             String
Library             Collections
Library             DatabaseLibrary
Suite Setup         Run Keywords    DBConnect       Log In      Open Products Page
Suite Teardown      Run Keywords    Log Out     Close All Browsers      DBDisconnect


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
    Capture Page Screenshot     filename=test_open_add_product_page.png
    And entered product name and product title
    Capture Page Screenshot     filename=filled_product_name.png
    And entered product model
    Capture Page Screenshot     filename=filled_product_model.png
    When saved changes
    Then success alert is on page
    Capture Page Screenshot     filename=test_add_product_success_alert.png
    And product appeared in database

Test Delete Product
    Given found product     ${PRODUCT_NAME}
    Capture Page Screenshot     filename=found_product.png
    And chosen product
    Capture Page Screenshot     filename=chose_product.png
    When pushed product delete button
    Then success alert is on page
    Capture Page Screenshot     filename=test_delete_product_success_alert.png
    And products count changed to minus one

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
    Click Element   css:li#menu-catalog a
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

DBConnect
    Connect To Database    MySQLdb    opencart    ocuser    PASSWORD    127.0.0.1    3306
    log to console      Connected to DB

DBDisconnect
    Disconnect From Database
    log to console      DisConnected from DB

product appeared in database
    ${is_in_DB}=     Check If Exists In Database    SELECT * FROM oc_product WHERE model like '%Test%';
    log to console      ${PRODUCT_MODEL} appeared in DB
    ${products_count}=      products count
    should be equal as strings      ${products_count}   ((20,),)

products count
    ${output} =    Query    SELECT COUNT(*) FROM oc_product;
    [return]        ${output}

products count changed to minus one
    ${products_count}=      products count
    should be equal as strings      ${products_count}   ((19,),)
