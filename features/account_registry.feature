Feature: Account registry

  Scenario: User is able to create 2 accounts
    Given Account registry is empty
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101011234"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "79101011234" exists in registry

  Scenario: Created account has all fields correctly set
    Given Account registry is empty
    When I create an account using name: "adam", last name: "małysz", pesel: "92010109876"
    Then Account with pesel "92010109876" exists in registry
    And Account with pesel "92010109876" has "name" equal to "adam"
    And Account with pesel "92010109876" has "surname" equal to "małysz"
    And Account with pesel "92010109876" has "balance" equal to "0.0"

  Scenario: User is able to update surname of already created account
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "filatov"
    Then Account with pesel "95092909876" has "surname" equal to "filatov"

  Scenario: User is able to update name of already created account
    Given Account registry is empty
    And I create an account using name: "tomasz", last name: "niezgodny", pesel: "96092909876"
    When I update "name" of account with pesel: "96092909876" to "kamil"
    Then Account with pesel "96092909876" has "name" equal to "kamil"

  Scenario: User is able to delete created account
    Given Account registry is empty
    And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"

  Scenario: User is able to make incoming transfer
    Given Account registry is empty
    And I create an account using name: "jan", last name: "transferowy", pesel: "55555555555"
    When I make transfer of type "incoming" with amount "100" to account with pesel "55555555555"
    Then Account with pesel "55555555555" has "balance" equal to "100.0"

  Scenario: User is able to make outgoing transfer
    Given Account registry is empty
    And I create an account using name: "anna", last name: "bogata", pesel: "66666666666"
    And I make transfer of type "incoming" with amount "500" to account with pesel "66666666666"
    When I make transfer of type "outgoing" with amount "200" to account with pesel "66666666666"
    Then Account with pesel "66666666666" has "balance" equal to "300.0"