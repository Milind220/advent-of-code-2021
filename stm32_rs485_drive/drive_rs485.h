#ifndef DRIVE_RS485_H
#define DRIVE_RS485_H

#include <stdbool.h>
#include <stdint.h>

#include "stm32fxxx_hal.h"

#ifdef __cplusplus
extern "C" {
#endif

#define DRIVE_RS485_MAX_REGS 32U

#define DRIVE_RS485_ADDR_RESET_DRIVE 100U
#define DRIVE_RS485_ADDR_ENABLE_IO 101U
#define DRIVE_RS485_ADDR_MOTOR_STATUS 113U
#define DRIVE_RS485_ADDR_MOTOR_CURRENT 114U
#define DRIVE_RS485_ADDR_MOTOR_SPEED 116U
#define DRIVE_RS485_ADDR_TERMINAL_VOLTAGE 120U
#define DRIVE_RS485_ADDR_MOSFET_TEMP 122U

#define DRIVE_RS485_ADDR_TARGET_SPEED 72U

typedef enum {
  DRIVE_RS485_OK = 0,
  DRIVE_RS485_ERROR = 1,
  DRIVE_RS485_BAD_PARAM = 2,
  DRIVE_RS485_TIMEOUT = 3,
  DRIVE_RS485_CRC_ERROR = 4,
  DRIVE_RS485_EXCEPTION = 5
} DriveRs485_Status;

typedef struct {
  UART_HandleTypeDef *uart;
  GPIO_TypeDef *de_port;
  uint16_t de_pin;
  uint8_t device_address;
  uint32_t timeout_ms;
} DriveRs485_Handle;

DriveRs485_Status DriveRs485_ReadInputRegisters(DriveRs485_Handle *handle,
                                                uint16_t start_addr,
                                                uint16_t count,
                                                uint16_t *out_regs);

DriveRs485_Status DriveRs485_WriteHoldingRegisters(DriveRs485_Handle *handle,
                                                   uint16_t start_addr,
                                                   uint16_t count,
                                                   const uint16_t *values);

DriveRs485_Status DriveRs485_SetTargetSpeedRpm(DriveRs485_Handle *handle,
                                               int32_t rpm);

int32_t DriveRs485_CombineS32(uint16_t high_word, uint16_t low_word);
float DriveRs485_Q24ToFloat(int32_t raw_value);
float DriveRs485_Q24Times1000ToFloat(int32_t raw_value);
int32_t DriveRs485_SpeedRpmToRawQ24(int32_t rpm);

#ifdef __cplusplus
}
#endif

#endif
