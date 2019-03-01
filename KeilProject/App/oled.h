#ifndef _OLED_H
#define _OLED_H

#include "system.h"

#define OLED_ADDRESS	0x78 //通过调整0R电阻,屏可以0x78和0x7A两个地址 -- 默认0x78

extern void OLED_Write_Reg(uint8_t regAddr, uint8_t regData);
extern void OLED_WriteCmd(unsigned char I2C_Command);
extern void OLED_WriteDat(unsigned char I2C_Data);//写数据
extern void OLED_Init(void);
extern void OLED_SetPos(unsigned char x, unsigned char y); //设置起始点坐标
extern void OLED_Fill(unsigned char fill_Data);//全屏填充
extern void OLED_CLS(void);//清屏
extern void OLED_ON(void);
extern void OLED_OFF(void);
extern void OLED_ShowStr(unsigned char x, unsigned char y, unsigned char ch[], unsigned char TextSize);
extern void OLED_ShowCN(unsigned char x, unsigned char y, unsigned char N);
extern void OLED_DrawBMP(unsigned char x0,unsigned char y0,unsigned char x1,unsigned char y1,unsigned char BMP[]);





#endif
