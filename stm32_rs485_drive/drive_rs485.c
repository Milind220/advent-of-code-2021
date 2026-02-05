#include "drive_rs485.h"

#define DRIVE_RS485_FUNC_READ_INPUT_REGS 0x04U
#define DRIVE_RS485_FUNC_WRITE_MULTIPLE_REGS 0x10U
#define DRIVE_RS485_EXCEPTION_MASK 0x80U
#define DRIVE_RS485_RESPONSE_OVERHEAD 5U
#define DRIVE_RS485_WRITE_RESPONSE_LEN 8U

static void DriveRs485_SetTx(DriveRs485_Handle *handle) {
  HAL_GPIO_WritePin(handle->de_port, handle->de_pin, GPIO_PIN_SET);
}

static void DriveRs485_SetRx(DriveRs485_Handle *handle) {
  HAL_GPIO_WritePin(handle->de_port, handle->de_pin, GPIO_PIN_RESET);
}

static DriveRs485_Status DriveRs485_WaitFlag(UART_HandleTypeDef *uart,
                                             uint32_t flag,
                                             uint32_t timeout_ms) {
  uint32_t start = HAL_GetTick();
  while (__HAL_UART_GET_FLAG(uart, flag) == RESET) {
    if ((HAL_GetTick() - start) >= timeout_ms) {
      return DRIVE_RS485_TIMEOUT;
    }
  }
  return DRIVE_RS485_OK;
}

static uint16_t DriveRs485_Crc16(const uint8_t *data, uint16_t length) {
  uint16_t crc = 0xFFFFU;
  for (uint16_t i = 0; i < length; i++) {
    crc ^= data[i];
    for (uint8_t bit = 0; bit < 8U; bit++) {
      if ((crc & 0x0001U) != 0U) {
        crc = (crc >> 1U) ^ 0xA001U;
      } else {
        crc >>= 1U;
      }
    }
  }
  return crc;
}

static DriveRs485_Status DriveRs485_SendFrame(DriveRs485_Handle *handle,
                                              const uint8_t *frame,
                                              uint16_t length) {
  DriveRs485_SetTx(handle);
  if (HAL_UART_Transmit(handle->uart, (uint8_t *)frame, length, handle->timeout_ms) !=
      HAL_OK) {
    DriveRs485_SetRx(handle);
    return DRIVE_RS485_ERROR;
  }

  DriveRs485_Status status =
      DriveRs485_WaitFlag(handle->uart, UART_FLAG_TC, handle->timeout_ms);
  DriveRs485_SetRx(handle);
  return status;
}

static DriveRs485_Status DriveRs485_ReadFrame(DriveRs485_Handle *handle,
                                              uint8_t *frame,
                                              uint16_t length) {
  if (HAL_UART_Receive(handle->uart, frame, length, handle->timeout_ms) != HAL_OK) {
    return DRIVE_RS485_TIMEOUT;
  }
  return DRIVE_RS485_OK;
}

static bool DriveRs485_ValidateCrc(const uint8_t *frame, uint16_t length) {
  uint16_t expected = DriveRs485_Crc16(frame, length - 2U);
  uint16_t received = (uint16_t)frame[length - 2U] | ((uint16_t)frame[length - 1U] << 8U);
  return expected == received;
}

static DriveRs485_Status DriveRs485_ValidateResponse(const uint8_t *frame,
                                                     uint16_t length,
                                                     uint8_t device_addr,
                                                     uint8_t function_code) {
  if (length < 5U) {
    return DRIVE_RS485_ERROR;
  }
  if (frame[0] != device_addr) {
    return DRIVE_RS485_ERROR;
  }
  if ((frame[1] & DRIVE_RS485_EXCEPTION_MASK) != 0U) {
    return DRIVE_RS485_EXCEPTION;
  }
  if (frame[1] != function_code) {
    return DRIVE_RS485_ERROR;
  }
  if (!DriveRs485_ValidateCrc(frame, length)) {
    return DRIVE_RS485_CRC_ERROR;
  }
  return DRIVE_RS485_OK;
}

static DriveRs485_Status DriveRs485_CheckHandle(const DriveRs485_Handle *handle) {
  if (handle == NULL || handle->uart == NULL || handle->de_port == NULL) {
    return DRIVE_RS485_BAD_PARAM;
  }
  if (handle->device_address == 0U) {
    return DRIVE_RS485_BAD_PARAM;
  }
  if (handle->timeout_ms == 0U) {
    return DRIVE_RS485_BAD_PARAM;
  }
  return DRIVE_RS485_OK;
}

DriveRs485_Status DriveRs485_ReadInputRegisters(DriveRs485_Handle *handle,
                                                uint16_t start_addr,
                                                uint16_t count,
                                                uint16_t *out_regs) {
  DriveRs485_Status status = DriveRs485_CheckHandle(handle);
  if (status != DRIVE_RS485_OK) {
    return status;
  }
  if (out_regs == NULL || count == 0U || count > DRIVE_RS485_MAX_REGS) {
    return DRIVE_RS485_BAD_PARAM;
  }

  uint8_t request[8];
  request[0] = handle->device_address;
  request[1] = DRIVE_RS485_FUNC_READ_INPUT_REGS;
  request[2] = (uint8_t)(start_addr >> 8U);
  request[3] = (uint8_t)(start_addr & 0xFFU);
  request[4] = (uint8_t)(count >> 8U);
  request[5] = (uint8_t)(count & 0xFFU);
  uint16_t crc = DriveRs485_Crc16(request, 6U);
  request[6] = (uint8_t)(crc & 0xFFU);
  request[7] = (uint8_t)(crc >> 8U);

  status = DriveRs485_SendFrame(handle, request, sizeof(request));
  if (status != DRIVE_RS485_OK) {
    return status;
  }

  uint16_t response_len = (uint16_t)(DRIVE_RS485_RESPONSE_OVERHEAD + (count * 2U));
  uint8_t response[DRIVE_RS485_RESPONSE_OVERHEAD + (DRIVE_RS485_MAX_REGS * 2U)];
  status = DriveRs485_ReadFrame(handle, response, response_len);
  if (status != DRIVE_RS485_OK) {
    return status;
  }

  status = DriveRs485_ValidateResponse(response, response_len, handle->device_address,
                                       DRIVE_RS485_FUNC_READ_INPUT_REGS);
  if (status != DRIVE_RS485_OK) {
    return status;
  }

  if (response[2] != (uint8_t)(count * 2U)) {
    return DRIVE_RS485_ERROR;
  }

  for (uint16_t i = 0; i < count; i++) {
    uint16_t index = (uint16_t)(3U + (i * 2U));
    out_regs[i] = (uint16_t)((response[index] << 8U) | response[index + 1U]);
  }
  return DRIVE_RS485_OK;
}

DriveRs485_Status DriveRs485_WriteHoldingRegisters(DriveRs485_Handle *handle,
                                                   uint16_t start_addr,
                                                   uint16_t count,
                                                   const uint16_t *values) {
  DriveRs485_Status status = DriveRs485_CheckHandle(handle);
  if (status != DRIVE_RS485_OK) {
    return status;
  }
  if (values == NULL || count == 0U || count > DRIVE_RS485_MAX_REGS) {
    return DRIVE_RS485_BAD_PARAM;
  }

  uint8_t request[9U + (DRIVE_RS485_MAX_REGS * 2U)];
  uint16_t payload_len = (uint16_t)(7U + (count * 2U));

  request[0] = handle->device_address;
  request[1] = DRIVE_RS485_FUNC_WRITE_MULTIPLE_REGS;
  request[2] = (uint8_t)(start_addr >> 8U);
  request[3] = (uint8_t)(start_addr & 0xFFU);
  request[4] = (uint8_t)(count >> 8U);
  request[5] = (uint8_t)(count & 0xFFU);
  request[6] = (uint8_t)(count * 2U);

  for (uint16_t i = 0; i < count; i++) {
    uint16_t index = (uint16_t)(7U + (i * 2U));
    request[index] = (uint8_t)(values[i] >> 8U);
    request[index + 1U] = (uint8_t)(values[i] & 0xFFU);
  }

  uint16_t crc = DriveRs485_Crc16(request, payload_len);
  request[payload_len] = (uint8_t)(crc & 0xFFU);
  request[payload_len + 1U] = (uint8_t)(crc >> 8U);

  status = DriveRs485_SendFrame(handle, request, (uint16_t)(payload_len + 2U));
  if (status != DRIVE_RS485_OK) {
    return status;
  }

  uint8_t response[DRIVE_RS485_WRITE_RESPONSE_LEN];
  status = DriveRs485_ReadFrame(handle, response, sizeof(response));
  if (status != DRIVE_RS485_OK) {
    return status;
  }

  status = DriveRs485_ValidateResponse(response, sizeof(response), handle->device_address,
                                       DRIVE_RS485_FUNC_WRITE_MULTIPLE_REGS);
  if (status != DRIVE_RS485_OK) {
    return status;
  }

  return DRIVE_RS485_OK;
}

DriveRs485_Status DriveRs485_SetTargetSpeedRpm(DriveRs485_Handle *handle, int32_t rpm) {
  int32_t raw = DriveRs485_SpeedRpmToRawQ24(rpm);
  uint16_t values[2];
  values[0] = (uint16_t)((uint32_t)raw >> 16U);
  values[1] = (uint16_t)((uint32_t)raw & 0xFFFFU);
  return DriveRs485_WriteHoldingRegisters(handle, DRIVE_RS485_ADDR_TARGET_SPEED, 2U, values);
}

int32_t DriveRs485_CombineS32(uint16_t high_word, uint16_t low_word) {
  uint32_t combined = ((uint32_t)high_word << 16U) | (uint32_t)low_word;
  return (int32_t)combined;
}

float DriveRs485_Q24ToFloat(int32_t raw_value) {
  return (float)raw_value / 16777216.0f;
}

float DriveRs485_Q24Times1000ToFloat(int32_t raw_value) {
  return ((float)raw_value * 1000.0f) / 16777216.0f;
}

int32_t DriveRs485_SpeedRpmToRawQ24(int32_t rpm) {
  return (int32_t)(((int64_t)rpm * 16777216LL) / 1000LL);
}
