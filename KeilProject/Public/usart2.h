#ifndef _USART2_H
#define _USART2_H

#include "system.h"
#include "stdio.h"

extern void USART2_Init(u32 baud);
//extern int fputc(int ch, FILE *p);
#define USART2_MAX_QUEUE_BUF_SIZE 100	//USART2串口缓冲区大小，单位：字节

extern uint8_t USART2_RECEIEVE_QUEUE_BUF[USART2_MAX_QUEUE_BUF_SIZE];//USART2串口缓冲区
extern uint8_t USART2_QUEUE_REAR;//串口缓冲区队列尾，入队位置
extern uint8_t USART2_QUEUE_FRONT;//串口缓冲区队列首，出队位置
extern uint8_t USART2_QUEUE_FULL(void);
extern uint8_t USART2_QUEUE_EMPTY(void);
extern uint8_t USART2_PUSH_QUEUE(uint8_t ch);
extern uint8_t USART2_POP_QUEUE(void);
extern void USART2_WriteByte(uint8_t ch);
extern void USART2_WriteBytes(uint8_t n, uint8_t *p);


#endif
