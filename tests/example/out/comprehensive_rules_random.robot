# ============================================================================
# TEST COVERAGE INFORMATION
# ============================================================================
#
# Covered states (6/8):
#     Alert
#     Critical
#     Monitoring
#     Normal
#     Shutdown
#     Warning
#
# Covered actions (23/33):
#     acknowledge alert  (Alert -> Monitoring)
#     check humidity  (Monitoring -> Normal)
#     check load  (Monitoring -> Alert)
#     continue monitoring  (Normal -> Monitoring)
#     crisis management  (Critical -> Monitoring)
#     emergency protocol  (Alert -> Monitoring)
#     emergency shutdown  (Critical -> Shutdown)
#     escalate alert  (Alert -> Critical)
#     escalate warning  (Warning -> Alert)
#     maintenance mode  (Shutdown -> Monitoring)
#     manual override  (Critical -> Monitoring)
#     monitor alerts  (Monitoring -> Normal)
#     monitor pressure  (Monitoring -> Alert)
#     monitor response  (Monitoring -> Warning)
#     read humidity  (Monitoring -> Alert)
#     read temperature  (Monitoring -> Normal)
#     read temperature  (Monitoring -> Alert)
#     review warning  (Warning -> Monitoring)
#     run diagnostics  (Normal -> Monitoring)
#     schedule maintenance  (Normal -> Monitoring)
#     sensor check  (Monitoring -> Normal)
#     sensor check  (Monitoring -> Normal)
#     validate sensor  (Monitoring -> Alert)
#
# Uncovered states (2/8):
#     Initialization
#     Start
#
# Uncovered actions (10/33):
#     calibrate system (Initialization -> Monitoring)
#     check pressure (Monitoring -> Alert)
#     check sensors (Initialization -> Monitoring)
#     emergency mode (Initialization -> Monitoring)
#     initialize system (Start -> Initialization)
#     investigate issue (Warning -> Monitoring)
#     read temperature (Monitoring -> Warning)
#     read temperature (Monitoring -> Normal)
#     restart system (Shutdown -> Start)
#     start diagnostics (Initialization -> Monitoring)
#
# ============================================================================

*** Settings ***
Library         ../ExampleLibrary.py


*** Test Cases ***
Test 1
  Set Machine Variables  25  60  1020  normal  humid02  test  5  1000  low
  continue monitoring
  sensor check
  continue monitoring
  monitor response
  escalate warning
  escalate alert
  crisis management
  sensor check
  continue monitoring
  monitor response
  escalate warning
  escalate alert
  crisis management
  monitor response
  escalate warning
  escalate alert
  crisis management
  check load
  escalate alert
  crisis management

Test 2
  Set Machine Variables  20  60  990  warning  temp01  auto  3  200  medium
  continue monitoring
  read humidity
  acknowledge alert
  sensor check
  continue monitoring
  validate sensor
  acknowledge alert
  read humidity
  acknowledge alert
  read temperature
  continue monitoring
  monitor response
  escalate warning
  acknowledge alert
  monitor response
  escalate warning
  acknowledge alert
  sensor check
  continue monitoring
  read humidity

Test 3
  Set Machine Variables  35  70  990  critical  humid01  test  3  500  low
  continue monitoring
  validate sensor
  acknowledge alert
  validate sensor
  acknowledge alert
  monitor response
  escalate warning
  acknowledge alert
  monitor response
  escalate warning
  acknowledge alert
  read temperature
  acknowledge alert
  sensor check
  continue monitoring
  sensor check
  continue monitoring
  read temperature
  acknowledge alert
  read temperature

Test 4
  Set Machine Variables  25  50  1000  critical  press01  auto  2  2000  low
  continue monitoring
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  monitor response
  review warning
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity

Test 5
  Set Machine Variables  30  50  1010  emergency  humid01  test  4  2000  critical
  continue monitoring
  monitor response
  escalate warning
  emergency protocol
  monitor response
  escalate warning
  emergency protocol
  validate sensor
  escalate alert
  emergency shutdown

Test 6
  Set Machine Variables  15  40  990  warning  temp01  maintenance  5  100  critical
  schedule maintenance
  sensor check
  schedule maintenance
  monitor pressure
  escalate alert
  emergency shutdown
  maintenance mode
  sensor check
  schedule maintenance
  check humidity
  continue monitoring
  check humidity
  continue monitoring
  sensor check
  schedule maintenance
  check humidity
  continue monitoring
  check load
  escalate alert
  crisis management

Test 7
  Set Machine Variables  35  50  1010  emergency  press01  test  3  200  high
  continue monitoring
  monitor response
  escalate warning
  acknowledge alert
  read temperature
  emergency protocol
  monitor response
  escalate warning
  emergency protocol
  read humidity
  emergency protocol
  read temperature
  emergency protocol
  monitor response
  escalate warning
  acknowledge alert
  read temperature
  acknowledge alert
  read humidity
  emergency protocol

Test 8
  Set Machine Variables  20  60  1010  critical  humid01  maintenance  2  2000  low
  continue monitoring
  monitor response
  review warning
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read temperature
  continue monitoring
  validate sensor
  acknowledge alert
  monitor response
  review warning
  validate sensor
  acknowledge alert
  read temperature
  schedule maintenance
  monitor response
  review warning
  read temperature

Test 9
  Set Machine Variables  35  80  1030  warning  temp01  auto  1  200  critical
  continue monitoring
  monitor pressure
  acknowledge alert
  monitor response
  review warning
  read temperature
  acknowledge alert
  monitor pressure
  acknowledge alert
  monitor response
  review warning
  sensor check
  continue monitoring
  validate sensor
  acknowledge alert
  read humidity
  acknowledge alert
  monitor pressure
  acknowledge alert
  read temperature

Test 10
  Set Machine Variables  20  60  1000  emergency  humid02  maintenance  2  500  high
  continue monitoring
  read temperature
  schedule maintenance
  read humidity
  emergency protocol
  read humidity
  acknowledge alert
  sensor check
  continue monitoring
  read temperature
  continue monitoring
  validate sensor
  emergency protocol
  sensor check
  schedule maintenance
  monitor response
  review warning
  monitor response
  review warning
  validate sensor

Test 11
  Set Machine Variables  40  50  990  emergency  temp01  manual  3  100  critical
  continue monitoring
  validate sensor
  emergency protocol
  read temperature
  acknowledge alert
  sensor check
  continue monitoring
  monitor pressure
  emergency protocol
  monitor pressure
  emergency protocol
  read temperature
  acknowledge alert
  read temperature
  emergency protocol
  monitor pressure
  emergency protocol
  read humidity
  acknowledge alert
  read humidity

Test 12
  Set Machine Variables  40  40  1000  critical  temp01  test  4  200  high
  continue monitoring
  check humidity
  continue monitoring
  check load
  escalate alert
  crisis management
  read humidity
  escalate alert
  crisis management
  monitor response
  escalate warning
  escalate alert
  crisis management
  check load
  escalate alert
  crisis management
  validate sensor
  escalate alert
  crisis management
  check load

Test 13
  Set Machine Variables  30  50  990  critical  temp01  manual  1  1000  low
  continue monitoring
  monitor pressure
  acknowledge alert
  monitor response
  review warning
  validate sensor
  acknowledge alert
  monitor response
  review warning
  sensor check
  continue monitoring
  monitor alerts
  continue monitoring
  sensor check
  continue monitoring
  validate sensor
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity

Test 14
  Set Machine Variables  25  30  1010  normal  temp02  test  3  1000  high
  continue monitoring
  check humidity
  continue monitoring
  validate sensor
  acknowledge alert
  validate sensor
  acknowledge alert
  monitor response
  escalate warning
  acknowledge alert
  sensor check
  continue monitoring
  check humidity
  continue monitoring
  read humidity
  acknowledge alert
  monitor response
  escalate warning
  acknowledge alert
  monitor response

Test 15
  Set Machine Variables  35  90  1000  emergency  humid01  maintenance  3  500  high
  schedule maintenance
  read temperature
  acknowledge alert
  monitor response
  escalate warning
  acknowledge alert
  monitor response
  escalate warning
  emergency protocol
  monitor response
  escalate warning
  emergency protocol
  read temperature
  emergency protocol
  monitor response
  escalate warning
  acknowledge alert
  read temperature
  acknowledge alert
  monitor response

Test 16
  Set Machine Variables  15  30  1020  critical  humid02  manual  1  100  medium
  continue monitoring
  validate sensor
  acknowledge alert
  read humidity
  acknowledge alert
  sensor check
  continue monitoring
  sensor check
  continue monitoring
  read humidity
  acknowledge alert
  validate sensor
  acknowledge alert
  sensor check
  continue monitoring
  check humidity
  continue monitoring
  check humidity
  continue monitoring
  sensor check

Test 17
  Set Machine Variables  15  50  990  emergency  temp01  manual  1  100  low
  continue monitoring
  monitor alerts
  continue monitoring
  monitor pressure
  emergency protocol
  read humidity
  emergency protocol
  monitor alerts
  continue monitoring
  monitor pressure
  acknowledge alert
  read temperature
  continue monitoring
  monitor alerts
  continue monitoring
  monitor pressure
  acknowledge alert
  read temperature
  continue monitoring
  monitor pressure

Test 18
  Set Machine Variables  15  70  1020  emergency  temp02  auto  3  500  low
  continue monitoring
  validate sensor
  acknowledge alert
  read humidity
  acknowledge alert
  monitor response
  escalate warning
  emergency protocol
  read humidity
  acknowledge alert
  monitor response
  escalate warning
  emergency protocol
  validate sensor
  emergency protocol
  read humidity
  acknowledge alert
  read humidity
  emergency protocol
  monitor response

Test 19
  Set Machine Variables  40  80  1000  warning  press01  manual  3  1000  low
  continue monitoring
  read humidity
  acknowledge alert
  monitor response
  escalate warning
  acknowledge alert
  monitor response
  escalate warning
  acknowledge alert
  read humidity
  acknowledge alert
  monitor response
  escalate warning
  acknowledge alert
  read temperature
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert

Test 20
  Set Machine Variables  35  70  1010  emergency  humid01  auto  3  1000  medium
  continue monitoring
  validate sensor
  acknowledge alert
  read temperature
  acknowledge alert
  validate sensor
  acknowledge alert
  validate sensor
  acknowledge alert
  read humidity
  emergency protocol
  validate sensor
  emergency protocol
  read temperature
  emergency protocol
  read temperature
  acknowledge alert
  sensor check
  continue monitoring
  read temperature

Test 21
  Set Machine Variables  40  30  1020  critical  temp02  manual  5  1000  critical
  continue monitoring
  sensor check
  continue monitoring
  read humidity
  escalate alert
  emergency shutdown

Test 22
  Set Machine Variables  25  40  1030  warning  humid01  test  3  200  low
  continue monitoring
  check humidity
  continue monitoring
  check humidity
  continue monitoring
  check humidity
  continue monitoring
  read humidity
  acknowledge alert
  validate sensor
  acknowledge alert
  monitor pressure
  acknowledge alert
  sensor check
  continue monitoring
  monitor response
  escalate warning
  acknowledge alert
  monitor response
  escalate warning

Test 23
  Set Machine Variables  35  90  1020  emergency  temp01  auto  1  200  critical
  continue monitoring
  monitor response
  review warning
  monitor alerts
  continue monitoring
  read temperature
  acknowledge alert
  read humidity
  emergency protocol
  read humidity
  acknowledge alert
  monitor response
  review warning
  sensor check
  continue monitoring
  sensor check
  continue monitoring
  read humidity
  emergency protocol
  validate sensor

Test 24
  Set Machine Variables  15  30  1010  normal  humid02  maintenance  3  500  medium
  schedule maintenance
  read temperature
  continue monitoring
  monitor response
  escalate warning
  acknowledge alert
  validate sensor
  acknowledge alert
  sensor check
  schedule maintenance
  check humidity
  schedule maintenance
  read humidity
  acknowledge alert
  read temperature
  continue monitoring
  check humidity
  continue monitoring
  sensor check
  continue monitoring

Test 25
  Set Machine Variables  35  50  1030  warning  temp02  test  5  2000  medium
  continue monitoring
  monitor response
  escalate warning
  escalate alert
  crisis management
  monitor pressure
  escalate alert
  crisis management
  read temperature
  escalate alert
  crisis management
  check load
  escalate alert
  crisis management
  monitor response
  escalate warning
  escalate alert
  crisis management
  sensor check
  continue monitoring

Test 26
  Set Machine Variables  20  30  1000  normal  humid02  manual  2  200  critical
  continue monitoring
  read temperature
  continue monitoring
  monitor response
  review warning
  monitor response
  review warning
  read temperature
  continue monitoring
  check humidity
  continue monitoring
  validate sensor
  acknowledge alert
  read temperature
  continue monitoring
  sensor check
  continue monitoring
  check humidity
  continue monitoring
  read temperature

Test 27
  Set Machine Variables  30  40  990  normal  temp01  test  3  100  high
  continue monitoring
  validate sensor
  acknowledge alert
  monitor pressure
  acknowledge alert
  validate sensor
  acknowledge alert
  check humidity
  continue monitoring
  check humidity
  continue monitoring
  monitor pressure
  acknowledge alert
  monitor pressure
  acknowledge alert
  monitor pressure
  acknowledge alert
  monitor pressure
  acknowledge alert
  sensor check

Test 28
  Set Machine Variables  25  40  1010  warning  temp02  manual  5  1000  high
  continue monitoring
  read humidity
  escalate alert
  manual override
  validate sensor
  escalate alert
  crisis management
  check load
  escalate alert
  crisis management
  check humidity
  continue monitoring
  read humidity
  escalate alert
  crisis management
  monitor response
  escalate warning
  escalate alert
  crisis management
  monitor response

Test 29
  Set Machine Variables  20  90  1010  warning  humid01  test  0  500  high
  run diagnostics
  read temperature
  continue monitoring
  read humidity
  acknowledge alert
  monitor alerts
  run diagnostics
  read temperature
  continue monitoring
  sensor check
  continue monitoring
  read humidity
  acknowledge alert
  monitor response
  review warning
  sensor check
  continue monitoring
  read humidity
  acknowledge alert
  read temperature

Test 30
  Set Machine Variables  25  50  1020  normal  press01  auto  3  100  critical
  continue monitoring
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity

Test 31
  Set Machine Variables  40  60  1020  critical  temp01  maintenance  4  500  critical
  schedule maintenance
  check load
  escalate alert
  crisis management
  sensor check
  schedule maintenance
  read temperature
  escalate alert
  crisis management
  read temperature
  escalate alert
  crisis management
  monitor response
  escalate warning
  escalate alert
  crisis management
  read humidity
  escalate alert
  emergency shutdown
  maintenance mode

Test 32
  Set Machine Variables  40  80  990  emergency  humid02  maintenance  3  1000  critical
  continue monitoring
  sensor check
  continue monitoring
  read temperature
  emergency protocol
  monitor pressure
  emergency protocol
  monitor pressure
  acknowledge alert
  monitor pressure
  emergency protocol
  read humidity
  emergency protocol
  read humidity
  emergency protocol
  monitor response
  escalate warning
  emergency protocol
  read humidity
  emergency protocol

Test 33
  Set Machine Variables  40  60  1020  warning  humid01  maintenance  4  200  high
  continue monitoring
  check load
  escalate alert
  crisis management
  monitor response
  escalate warning
  escalate alert
  crisis management
  sensor check
  schedule maintenance
  check load
  escalate alert
  crisis management
  check load
  escalate alert
  crisis management
  check load
  escalate alert
  crisis management
  sensor check

Test 34
  Set Machine Variables  15  80  990  critical  humid01  test  0  200  medium
  run diagnostics
  read humidity
  acknowledge alert
  monitor response
  review warning
  monitor response
  review warning
  read temperature
  run diagnostics
  monitor response
  review warning
  monitor pressure
  acknowledge alert
  monitor response
  review warning
  read humidity
  acknowledge alert
  validate sensor
  acknowledge alert
  monitor pressure

Test 35
  Set Machine Variables  40  60  1020  critical  humid02  test  1  500  high
  continue monitoring
  monitor response
  review warning
  sensor check
  continue monitoring
  monitor alerts
  continue monitoring
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  monitor response
  review warning
  sensor check
  continue monitoring
  monitor alerts
  continue monitoring
  read temperature
  acknowledge alert
  monitor response

Test 36
  Set Machine Variables  25  60  1030  emergency  temp02  test  3  200  low
  continue monitoring
  read humidity
  acknowledge alert
  monitor pressure
  emergency protocol
  monitor response
  escalate warning
  emergency protocol
  read humidity
  acknowledge alert
  validate sensor
  emergency protocol
  read humidity
  acknowledge alert
  monitor pressure
  emergency protocol
  sensor check
  continue monitoring
  sensor check
  continue monitoring

Test 37
  Set Machine Variables  20  30  1020  warning  temp02  manual  2  2000  low
  continue monitoring
  read humidity
  acknowledge alert
  read temperature
  continue monitoring
  read temperature
  continue monitoring
  read temperature
  continue monitoring
  validate sensor
  acknowledge alert
  check humidity
  continue monitoring
  monitor response
  review warning
  validate sensor
  acknowledge alert
  read humidity
  acknowledge alert
  sensor check

Test 38
  Set Machine Variables  40  70  1000  critical  temp01  test  3  500  critical
  continue monitoring
  read humidity
  acknowledge alert
  sensor check
  continue monitoring
  validate sensor
  acknowledge alert
  validate sensor
  acknowledge alert
  sensor check
  continue monitoring
  sensor check
  continue monitoring
  monitor response
  escalate warning
  acknowledge alert
  monitor response
  escalate warning
  acknowledge alert
  read temperature

Test 39
  Set Machine Variables  20  90  1010  warning  humid01  maintenance  0  1000  high
  continue monitoring
  validate sensor
  acknowledge alert
  read temperature
  continue monitoring
  read humidity
  acknowledge alert
  validate sensor
  acknowledge alert
  monitor alerts
  continue monitoring
  monitor alerts
  run diagnostics
  monitor response
  review warning
  monitor alerts
  schedule maintenance
  validate sensor
  acknowledge alert
  validate sensor

Test 40
  Set Machine Variables  30  40  1010  critical  temp01  test  1  2000  low
  continue monitoring
  monitor alerts
  continue monitoring
  check humidity
  continue monitoring
  monitor alerts
  continue monitoring
  read humidity
  acknowledge alert
  monitor alerts
  continue monitoring
  check humidity
  continue monitoring
  monitor alerts
  continue monitoring
  read humidity
  acknowledge alert
  sensor check
  continue monitoring
  monitor response

Test 41
  Set Machine Variables  25  60  1010  warning  humid01  manual  1  1000  low
  continue monitoring
  monitor response
  review warning
  monitor alerts
  continue monitoring
  sensor check
  continue monitoring
  sensor check
  continue monitoring
  monitor alerts
  continue monitoring
  read humidity
  acknowledge alert
  sensor check
  continue monitoring
  sensor check
  continue monitoring
  read humidity
  acknowledge alert
  validate sensor

Test 42
  Set Machine Variables  30  40  1010  critical  temp02  auto  1  2000  medium
  continue monitoring
  check humidity
  continue monitoring
  read humidity
  acknowledge alert
  monitor response
  review warning
  validate sensor
  acknowledge alert
  sensor check
  continue monitoring
  sensor check
  continue monitoring
  sensor check
  continue monitoring
  monitor response
  review warning
  read humidity
  acknowledge alert
  monitor response

Test 43
  Set Machine Variables  25  60  1010  normal  humid02  auto  2  1000  critical
  continue monitoring
  read humidity
  acknowledge alert
  monitor response
  review warning
  validate sensor
  acknowledge alert
  read humidity
  acknowledge alert
  sensor check
  continue monitoring
  sensor check
  continue monitoring
  monitor response
  review warning
  validate sensor
  acknowledge alert
  sensor check
  continue monitoring
  monitor response

Test 44
  Set Machine Variables  30  30  1020  critical  humid02  maintenance  1  200  critical
  continue monitoring
  monitor response
  review warning
  read humidity
  acknowledge alert
  check humidity
  continue monitoring
  check humidity
  continue monitoring
  validate sensor
  acknowledge alert
  monitor alerts
  schedule maintenance
  sensor check
  schedule maintenance
  read humidity
  acknowledge alert
  monitor alerts
  schedule maintenance
  check humidity

Test 45
  Set Machine Variables  25  80  1030  warning  humid01  auto  1  100  medium
  continue monitoring
  monitor alerts
  continue monitoring
  validate sensor
  acknowledge alert
  sensor check
  continue monitoring
  monitor alerts
  continue monitoring
  monitor alerts
  continue monitoring
  monitor alerts
  continue monitoring
  sensor check
  continue monitoring
  monitor alerts
  continue monitoring
  sensor check
  continue monitoring
  sensor check

Test 46
  Set Machine Variables  35  40  1020  critical  humid01  manual  3  1000  critical
  continue monitoring
  read temperature
  acknowledge alert
  check humidity
  continue monitoring
  validate sensor
  acknowledge alert
  validate sensor
  acknowledge alert
  sensor check
  continue monitoring
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  sensor check
  continue monitoring
  monitor response

Test 47
  Set Machine Variables  25  40  1010  normal  humid01  manual  4  500  medium
  continue monitoring
  check humidity
  continue monitoring
  check load
  escalate alert
  crisis management
  sensor check
  continue monitoring
  monitor response
  escalate warning
  escalate alert
  crisis management
  check load
  escalate alert
  crisis management
  validate sensor
  escalate alert
  manual override
  check humidity
  continue monitoring

Test 48
  Set Machine Variables  20  70  990  emergency  humid02  manual  4  200  low
  continue monitoring
  read temperature
  continue monitoring
  sensor check
  continue monitoring
  sensor check
  continue monitoring
  validate sensor
  emergency protocol
  check load
  escalate alert
  manual override
  check load
  emergency protocol
  validate sensor
  emergency protocol
  read humidity
  emergency protocol
  validate sensor
  emergency protocol

Test 49
  Set Machine Variables  20  70  1010  warning  temp01  maintenance  4  100  medium
  schedule maintenance
  validate sensor
  escalate alert
  crisis management
  validate sensor
  escalate alert
  crisis management
  read humidity
  escalate alert
  crisis management
  validate sensor
  escalate alert
  crisis management
  validate sensor
  escalate alert
  crisis management
  read temperature
  continue monitoring
  validate sensor
  escalate alert

Test 50
  Set Machine Variables  40  30  990  emergency  temp01  auto  0  100  medium
  run diagnostics
  read temperature
  emergency protocol
  read temperature
  acknowledge alert
  read humidity
  acknowledge alert
  read humidity
  acknowledge alert
  monitor pressure
  emergency protocol
  read humidity
  emergency protocol
  read humidity
  emergency protocol
  read temperature
  acknowledge alert
  monitor pressure
  emergency protocol
  read humidity

*** Keywords ***
Set Machine Variables
  [Arguments]  ${TEMPERATURE}  ${HUMIDITY}  ${PRESSURE}  ${STATUS}  ${SENSOR_ID}  ${MODE}  ${ALERT_LEVEL}  ${RESPONSE_TIME}  ${SYSTEM_LOAD}
  Set Test Variable  \${TEMPERATURE}
  Set Test Variable  \${HUMIDITY}
  Set Test Variable  \${PRESSURE}
  Set Test Variable  \${STATUS}
  Set Test Variable  \${SENSOR_ID}
  Set Test Variable  \${MODE}
  Set Test Variable  \${ALERT_LEVEL}
  Set Test Variable  \${RESPONSE_TIME}
  Set Test Variable  \${SYSTEM_LOAD}
