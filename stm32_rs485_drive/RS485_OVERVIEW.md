# RS-485 overview (and how it relates to protocols)

## What RS-485 is (and is not)
RS-485 defines **only the physical/electrical layer** for serial communication over a differential pair (A/B). It does **not** define:
- Message framing
- Addressing
- Error checking
- Arbitration or who is allowed to talk when

Those behaviors come from the **protocol you run on top of RS-485** (for example, Modbus RTU, DMX512, or a custom UART-based protocol).

## Master-slave vs. multi-master
- In a **master-slave request/response protocol** (e.g., Modbus RTU), the **master is the only node that initiates frames**. Slaves respond only when addressed, so **bus arbitration is not needed**.
- In a **multi-master protocol**, multiple nodes might initiate traffic. In that case you must add **arbitration** (token passing, time slots, CSMA-style backoff, etc.). This is a protocol design choice, not an RS-485 requirement.

## What does an RS-485 “frame” look like?
There is **no universal RS-485 frame**. Most systems:
- Use standard **UART framing** (start bit, 8 data bits, optional parity, 1 stop bit), and
- Define higher-level “frames” in software.

Example (Modbus RTU) frame layout:
```
[Address][Function][Data...][CRC16]
```
Modbus RTU uses **silent intervals** between frames (3.5 character times) to delimit messages.

## How many bytes fit in a frame?
RS-485 itself does not limit frame length. Limits come from the **protocol**:
- **Modbus RTU** limits the **ADU (application data unit)** to **256 bytes total**, which includes address, function, data, and CRC.

## Practical notes
- RS-485 is typically **half-duplex** on two wires; only one node should drive the bus at a time.
- Proper **termination** and **biasing** resistors are required for reliable communication on longer lines or multi-drop networks.
- Because RS-485 is a physical layer, **your drive’s datasheet or protocol spec** is the source of truth for framing, limits, and timing.
