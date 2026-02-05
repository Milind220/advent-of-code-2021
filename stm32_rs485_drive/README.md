# STM32 RS485 Drive (Modbus RTU) Driver

Minimal STM32 HAL Modbus RTU master for the RS485 drive.

## Quick setup

1. UART: **9600 8N1**, no parity.
2. Wire RS485 DE (and optionally RE) to a GPIO.
3. Fill the handle and call the APIs.

## Example

```c
#include "drive_rs485.h"

static DriveRs485_Handle drive;

void Drive_Init(void) {
  drive.uart = &huart1;
  drive.de_port = RS485_DE_GPIO_Port;
  drive.de_pin = RS485_DE_Pin;
  drive.device_address = 1U;
  drive.timeout_ms = 100U;
}

void Drive_Task(void) {
  uint16_t regs[2];

  if (DriveRs485_ReadInputRegisters(&drive, DRIVE_RS485_ADDR_MOTOR_SPEED, 2U, regs) ==
      DRIVE_RS485_OK) {
    int32_t raw = DriveRs485_CombineS32(regs[0], regs[1]);
    float rpm = DriveRs485_Q24Times1000ToFloat(raw);
    (void)rpm;
  }

  (void)DriveRs485_SetTargetSpeedRpm(&drive, 1250);
}
```

## Notes

- Drive address defaults to `1`.
- Target speed uses Q24 scaling: `rpm * 2^24 / 1000`.
- Negative RPM values are allowed.
