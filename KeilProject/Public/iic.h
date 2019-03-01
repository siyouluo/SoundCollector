#ifndef _I2C_H
#define _I2C_H

#include "system.h"

/*  IIC_SCL时钟端口、引脚定义 */
#define IIC_SCL_PORT 			GPIOB   
#define IIC_SCL_PIN 			(GPIO_Pin_6)
#define IIC_SCL_PORT_RCC		RCC_APB2Periph_GPIOB

/*  IIC_SDA时钟端口、引脚定义 */
#define IIC_SDA_PORT 			GPIOB  
#define IIC_SDA_PIN 			(GPIO_Pin_7)
#define IIC_SDA_PORT_RCC		RCC_APB2Periph_GPIOB

//IO操作函数	 
#define IIC_SCL    PBout(6) //SCL
#define IIC_SDA    PBout(7) //SDA	 
#define READ_SDA   PBin(7)  //输入SDA

//IIC所有操作函数
void IIC_Init(void);                //初始化IIC的IO口				 
void IIC_Start(void);				//发送IIC开始信号
void IIC_Stop(void);	  			//发送IIC停止信号
void IIC_Write_Byte(u8 txd);			//IIC发送一个字节
u8 IIC_Read_Byte(u8 ack);//IIC读取一个字节
void IIC_Read_Bytes(uint8_t n, uint8_t *p);
u8 IIC_Wait_Ack(void); 				//IIC等待ACK信号
void IIC_Ack(void);					//IIC发送ACK信号
void IIC_NAck(void);				//IIC不发送ACK信号


#endif
