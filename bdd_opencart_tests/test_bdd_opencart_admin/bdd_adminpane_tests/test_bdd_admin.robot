*** Settings ***
Documentation       Simple Opencart tests using SeleniumLibrary.
Library             SeleniumLibrary     implicit_wait=5.0    screenshot_root_directory=test_bdd_admin_screens/
Library             String
Library             Collections
Suite Setup         Run Keywords    Log In      Open Menu
Suite Teardown      Run Keywords    Log Out     Close All Browsers


*** Variables ***
${LOGIN URL}        http://demo23.opencart.pro/admin/
${BROWSER}          Chrome
${LOGIN}            demo
${PASSWORD}         demo
${MANUFACTURERS}    xpath://a[contains(@href, 'route=catalog/manufacturer')]
${MANUFACTURER}     Apple


*** Test Cases ***
Test Find Manufacturer
    Open Manufacturers
    Find Manufacturer   ${MANUFACTURER}
    Log To Console  ${\n}Manufacturer ${MANUFACTURER} found
    Go Back

Last Order Info
    Get Last Order Date
    Get Last Order Sum

Last User Activity
    Get Last User Activity

Check Opencart Version
    Get Opencart Version

Is API Enabled
    Open API Page
    Check API status


*** Keywords ***
Log In
    Open Browser        ${LOGIN URL}    ${BROWSER}
    Input Username      ${LOGIN}
    Input Password      ${PASSWORD}
    Click Button        Войти

Log Out
    Click Link          Выход

Input Username
    [Arguments]     ${username}
    Input Text      username    ${username}

Input Password
    [Arguments]     ${password}
    Input Text      password    ${password}

Submit Credentials
    Click Button    Войти

Open Menu
    Click Element   id:button-menu

Open Manufacturers
    Click Element   partial link:Каталог
    Click Element   partial link:Производители

Find Manufacturer
    [Arguments]     ${manufacturer}
    Click Element   xpath://td[contains(@text, ${manufacturer})]

Open Admin Page
    Click Element   xpath://a[contains(@href, 'route=common')]

Get Opencart Version
    ${footer_text}  Get Text    id:footer
    ${version_line}     Split String    ${footer_text}      separator=\n
    ${version}      Split String    ${version_line}[2]     separator=
    Log To Console  ${version}[1]

Get Last Order Date
    ${table}      Get Table Cell      class:table   row=2   column=4
    log to console  ${\n}Last order date: ${table}

Get Last Order Sum
    ${table}      Get Table Cell      class:table   row=2   column=5
    log to console  ${\n}Last order sum: ${table}

Get Last User Activity
    ${activity_panel}   Get Text    class:list-group
    log to console      ${\n}${activity_panel}

Open API Page
    Click Element   partial link:Система
    Click Element   partial link:Пользователи
    Click Element   partial link:API

Check API status
    ${api_table}      Get Table Cell      class:table   row=2   column=3
    log to console  ${\n}API status: ${api_table}