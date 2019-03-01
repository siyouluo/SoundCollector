#ifndef _USART3_H
#define _USART3_H

#include "system.h"
#include "stdio.h"

#define USART3_MAX_QUEUE_BUF_SIZE 100	//USART3串口缓冲区大小，单位：字节

extern uint8_t USART3_RECEIEVE_QUEUE_BUF[USART3_MAX_QUEUE_BUF_SIZE];//USART3串口缓冲区
extern uint8_t USART3_QUEUE_REAR;//串口缓冲区队列尾，入队位置
extern uint8_t USART3_QUEUE_FRONT;//串口缓冲区队列首，出队位置
extern uint8_t USART3_QUEUE_FULL(void);
extern uint8_t USART3_QUEUE_EMPTY(void);
extern uint8_t USART3_PUSH_QUEUE(uint8_t ch);
extern uint8_t USART3_POP_QUEUE(void);




extern void USART3_Init(u32 baud);
//int fputc(int ch, FILE *p);
extern void USART3_WriteByte(uint8_t ch);
extern void USART3_WriteBytes(uint8_t n, uint8_t *p);


#endif
