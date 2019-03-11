#ifndef _ADC_H
#define _ADC_H

#include "system.h"

extern void ADCx_Init(void);
extern u16 Get_ADC_Value(u8 ch);


#define ADC_MAX_QUEUE_BUF_SIZE 100	//USART3串口缓冲区大小，单位：字节

//extern uint8_t ADC_QUEUE_BUF[ADC_MAX_QUEUE_BUF_SIZE];//USART3串口缓冲区
//extern uint8_t ADC_QUEUE_REAR;//串口缓冲区队列尾，入队位置
//extern uint8_t ADC_QUEUE_FRONT;//串口缓冲区队列首，出队位置
extern uint8_t ADC_QUEUE_FULL(void);
extern uint8_t ADC_QUEUE_EMPTY(void);
extern uint8_t ADC_PUSH_QUEUE(uint8_t ch);
extern uint8_t ADC_POP_QUEUE(void);
void ADC_CLEAR_QUEUE(void);
	
#endif
