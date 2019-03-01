#include "oled.h"
#include "SysTick.h"
#include "iic.h"
#include "oled_displaylib.h"


/**往OLED的寄存器中写入一个字节
 *@macro OLED_ADDRESS	:	OLED设备地址
 *@param regAddr		:	寄存器地址
 *@param regData		:	写入的字节数据
 */
void OLED_Write_Reg(uint8_t regAddr, uint8_t regData)
{
    //发送起始信号
    IIC_Start();
    //发送设备地址
    IIC_Write_Byte(OLED_ADDRESS);
    if(IIC_Wait_Ack())	goto stop;
    //发送寄存器地址
    IIC_Write_Byte(regAddr);
    if(IIC_Wait_Ack())	goto stop;
    //写数据到寄存器
    IIC_Write_Byte(regData);
    if(IIC_Wait_Ack())	goto stop;

stop:
    IIC_Stop();
}

void OLED_WriteCmd(unsigned char I2C_Command)//写命令
{
    OLED_Write_Reg(0x00, I2C_Command);
}

void OLED_WriteDat(unsigned char I2C_Data)//写数据
{
    OLED_Write_Reg(0x40, I2C_Data);
}

void OLED_Init(void)
{
    delay_ms(100); //这里的延时很重要

    OLED_WriteCmd(0xAE); //display off
    OLED_WriteCmd(0x20);	//Set Memory Addressing Mode
    OLED_WriteCmd(0x10);	//00,Horizontal Addressing Mode;01,Vertical Addressing Mode;10,Page Addressing Mode (RESET);11,Invalid
    OLED_WriteCmd(0xb0);	//Set Page Start Address for Page Addressing Mode,0-7
    OLED_WriteCmd(0xc8);	//Set COM Output Scan Direction
    OLED_WriteCmd(0x00); //---set low column address
    OLED_WriteCmd(0x10); //---set high column address
    OLED_WriteCmd(0x40); //--set start line address
    OLED_WriteCmd(0x81); //--set contrast control register
    OLED_WriteCmd(0xff); //亮度调节 0x00~0xff
    OLED_WriteCmd(0xa1); //--set segment re-map 0 to 127
    OLED_WriteCmd(0xa6); //--set normal display
    OLED_WriteCmd(0xa8); //--set multiplex ratio(1 to 64)
    OLED_WriteCmd(0x3F); //
    OLED_WriteCmd(0xa4); //0xa4,Output follows RAM content;0xa5,Output ignores RAM content
    OLED_WriteCmd(0xd3); //-set display offset
    OLED_WriteCmd(0x00); //-not offset
    OLED_WriteCmd(0xd5); //--set display clock divide ratio/oscillator frequency
    OLED_WriteCmd(0xf0); //--set divide ratio
    OLED_WriteCmd(0xd9); //--set pre-charge period
    OLED_WriteCmd(0x22); //
    OLED_WriteCmd(0xda); //--set com pins hardware configuration
    OLED_WriteCmd(0x12);
    OLED_WriteCmd(0xdb); //--set vcomh
    OLED_WriteCmd(0x20); //0x20,0.77xVcc
    OLED_WriteCmd(0x8d); //--set DC-DC enable
    OLED_WriteCmd(0x14); //
    OLED_WriteCmd(0xaf); //--turn on oled panel
}

void OLED_SetPos(unsigned char x, unsigned char y) //设置起始点坐标
{
    OLED_WriteCmd(0xb0+y);
    OLED_WriteCmd(((x&0xf0)>>4)|0x10);
    OLED_WriteCmd((x&0x0f)|0x01);
}

void OLED_Fill(unsigned char fill_Data)//全屏填充
{
    unsigned char m,n;
    for(m=0; m<8; m++)
    {
        OLED_WriteCmd(0xb0+m);		//page0-page1
        OLED_WriteCmd(0x00);		//low column start address
        OLED_WriteCmd(0x10);		//high column start address
        for(n=0; n<128; n++)
        {
            OLED_WriteDat(fill_Data);
        }
    }
}

void OLED_CLS(void)//清屏
{
    OLED_Fill(0x00);
}

//--------------------------------------------------------------
// Prototype      : void OLED_ON(void)
// Calls          :
// Parameters     : none
// Description    : 将OLED从休眠中唤醒
//--------------------------------------------------------------
void OLED_ON(void)
{
    OLED_WriteCmd(0X8D);  //设置电荷泵
    OLED_WriteCmd(0X14);  //开启电荷泵
    OLED_WriteCmd(0XAF);  //OLED唤醒
}

//--------------------------------------------------------------
// Prototype      : void OLED_OFF(void)
// Calls          :
// Parameters     : none
// Description    : 让OLED休眠 -- 休眠模式下,OLED功耗不到10uA
//--------------------------------------------------------------
void OLED_OFF(void)
{
    OLED_WriteCmd(0X8D);  //设置电荷泵
    OLED_WriteCmd(0X10);  //关闭电荷泵
    OLED_WriteCmd(0XAE);  //OLED休眠
}

//--------------------------------------------------------------
// Prototype      : void OLED_ShowChar(unsigned char x, unsigned char y, unsigned char ch[], unsigned char TextSize)
// Calls          :
// Parameters     : x,y -- 起始点坐标(x:0~127, y:0~7); ch[] -- 要显示的字符串; TextSize -- 字符大小(1:6*8 ; 2:8*16)
// Description    : 显示codetab.h中的ASCII字符,有6*8和8*16可选择
//--------------------------------------------------------------
void OLED_ShowStr(unsigned char x, unsigned char y, unsigned char ch[], unsigned char TextSize)
{
    unsigned char c = 0,i = 0,j = 0;
    switch(TextSize)
    {
    case 1:
    {
        while(ch[j] != '\0')
        {
            c = ch[j] - 32;
            if(x > 126)
            {
                x = 0;
                y++;
            }
            OLED_SetPos(x,y);
            for(i=0; i<6; i++)
                OLED_WriteDat(F6x8[c][i]);
            x += 6;
            j++;
        }
    }
    break;
    case 2:
    {
        while(ch[j] != '\0')
        {
            c = ch[j] - 32;
            if(x > 120)
            {
                x = 0;
                y++;
            }
            OLED_SetPos(x,y);
            for(i=0; i<8; i++)
                OLED_WriteDat(F8X16[c*16+i]);
            OLED_SetPos(x,y+1);
            for(i=0; i<8; i++)
                OLED_WriteDat(F8X16[c*16+i+8]);
            x += 8;
            j++;
        }
    }
    break;
    }
}

//--------------------------------------------------------------
// Prototype      : void OLED_ShowCN(unsigned char x, unsigned char y, unsigned char N)
// Calls          :
// Parameters     : x,y -- 起始点坐标(x:0~127, y:0~7); N:汉字在codetab.h中的索引
// Description    : 显示codetab.h中的汉字,16*16点阵
//--------------------------------------------------------------
void OLED_ShowCN(unsigned char x, unsigned char y, unsigned char N)
{
    unsigned char wm=0;
    unsigned int  adder=32*N;
    OLED_SetPos(x, y);
    for(wm = 0; wm < 16; wm++)
    {
        OLED_WriteDat(F16x16[adder]);
        adder += 1;
    }
    OLED_SetPos(x,y + 1);
    for(wm = 0; wm < 16; wm++)
    {
        OLED_WriteDat(F16x16[adder]);
        adder += 1;
    }
}

//--------------------------------------------------------------
// Prototype      : void OLED_DrawBMP(unsigned char x0,unsigned char y0,unsigned char x1,unsigned char y1,unsigned char BMP[]);
// Calls          :
// Parameters     : x0,y0 -- 起始点坐标(x0:0~127, y0:0~7); x1,y1 -- 起点对角线(结束点)的坐标(x1:1~128,y1:1~8)
// Description    : 显示BMP位图
//--------------------------------------------------------------
void OLED_DrawBMP(unsigned char x0,unsigned char y0,unsigned char x1,unsigned char y1,unsigned char BMP[])
{
    unsigned int j=0;
    unsigned char x,y;

    if(y1%8==0)
        y = y1/8;
    else
        y = y1/8 + 1;
    for(y=y0; y<y1; y++)
    {
        OLED_SetPos(x0,y);
        for(x=x0; x<x1; x++)
        {
            OLED_WriteDat(BMP[j++]);
        }
    }
}


