-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Identify the suspect


-- query the description first to find out some suggestion tabout the clue.
-- SELECT
-- CRUD
SELECT description FROM crime_scene_reports
WHERE year = 2021 AND  month = 7 AND day = 28;

SELECT transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28
AND transcript LIKE '%bakery%';



--CReate
--Read
--Update
--Delete


--  car in 10:15 - 10:25

SELECT bakery_security_logs.activity, bakery_security_logs.license_plate, people.name
FROM people JOIN bakery_security_logs ON
bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2021 AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 15
AND bakery_security_logs.minute <= 25;


--TODO
-- # witness 2 what does she say.
-- transaction_type
SELECT people.name, atm_transactions.transaction_type
FROM people JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number
= bank_accounts.account_number WHERE atm_transactions.year = 2021
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_location = "Leggett Street";


-- how to do all the stuff together -> JOIN


--todo

-- ALTER TABLE phone_calls
-- ADD caller_name text;

-- ALTER TABLE phone_calls
-- ADD receiver_name text;


UPDATE phone_calls SET caller_name = people.name
FROM people WHERE phone_calls.caller = people.phone_number;

UPDATE phone_calls SET receiver_name = people.name
FROM people WHERE phone_calls.receiver = people.phone_number;

SELECT caller,caller_name ,receiver ,receiver_name FROM phone_calls

WHERE year = 2021

AND month = 7
AND day = 28
AND duration < 60;

-- next query the flight data find the earlist




--  find the location



SELECT id, hour, minute, origin_airport_id, destination_airport_id

FROM flights

WHERE year = 2021 AND month = 7 AND day = 29

ORDER BY hour ASC

LIMIT 1; -- first flight



SELECT city FROM airports WHERE id =
    (
    SELECT destination_airport_id FROM flights

    WHERE year = 2021 AND month = 7 AND day = 29

    ORDER BY hour ASC

    LIMIT 1);

SELECT flights.destination_airport_id, name, phone_number, license_plate
FROM people JOIN passengers ON  people.passport_number = passengers.passport_number
JOIN flights ON flights.id = passengers.flight_id WHERE flights.id = 36
ORDER BY flights.hour ASC ;


-- Bruce is the thief
-- he called Robin, so Robin is the accomplice
--the airport is airport no.4
-- which is Nwe York City!