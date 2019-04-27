#include "usart2.h"
#include "adc.h"
#include "timer.h"
uint8_t USART2_RECEIEVE_QUEUE_BUF[USART2_MAX_QUEUE_BUF_SIZE];//USART2串口缓冲区
uint8_t USART2_QUEUE_REAR=0;//串口缓冲区队列尾，入队位置
uint8_t USART2_QUEUE_FRONT=0;//串口缓冲区队列首，出队位置
/**
  * @brief :判断USART2串口缓冲区是否满
  * @param :void
  * @retval :返回1:满 返回0:非满
  * @usage:if(USART2_QUEUE_FULL()==1)...	if(USART2_QUEUE_FULL()==0)...
  */
uint8_t  USART2_QUEUE_FULL(void)
{
    return (uint8_t)(((USART2_QUEUE_REAR+1)% USART2_MAX_QUEUE_BUF_SIZE)==USART2_QUEUE_FRONT);
}


/**
  * @brief	:判断USART2串口缓冲区是否空
  * @param	:void
  * @retval	:返回1:空 返回0:非空
  * @usage	:if(USART2_QUEUE_EMPTY()==1)...	if(USART2_QUEUE_EMPTY()==0)...
  */
uint8_t USART2_QUEUE_EMPTY(void)
{
    return (uint8_t)(USART2_QUEUE_REAR==USART2_QUEUE_FRONT);
}

/**
  * @brief	:往USART2串口缓冲区内存入一个字节数据
  * @param	ch: uint8_t类型，写入ch
  * @retval	:1,队列满，写入失败；0，写入成功
  * @usage	:USART2_PUSH_QUEUE(0x3f)
  */
uint8_t USART2_PUSH_QUEUE(uint8_t ch)
{
    if(USART2_QUEUE_FULL())
    {
        printf("queue full!\n");
        return 1;
    }
    USART2_QUEUE_REAR=(USART2_QUEUE_REAR+1) % USART2_MAX_QUEUE_BUF_SIZE;
    USART2_RECEIEVE_QUEUE_BUF[USART2_QUEUE_REAR]=ch;
    return 0;
}
/**
  * @brief	:从USART2串口缓冲区取出一个字节数据
  * @param	:void
  * @retval	:uint8_t 类型，即为从缓冲区取出的字节
  * @usage	:uint8_t temp;
  * @usage	:temp=USART2_POP_QUEUE();
  */
uint8_t USART2_POP_QUEUE(void)
{
    uint8_t temp;
    if(USART2_QUEUE_EMPTY())
    {
        printf("queue empty!\n");
        return 1;
    }
    USART2_QUEUE_FRONT = (USART2_QUEUE_FRONT+1)%USART2_MAX_QUEUE_BUF_SIZE;
    temp = USART2_RECEIEVE_QUEUE_BUF[USART2_QUEUE_FRONT];
    return temp;
}
//int fputc(int ch, FILE *p)
//{
//	USART_SendData(USART2,(u8)ch);
//	while(USART_GetFlagStatus(USART2,USART_FLAG_TC) != SET);
//	return ch;
//}

void USART2_WriteByte(uint8_t ch)
{
	USART_SendData(USART2,(u8)ch);
	while(USART_GetFlagStatus(USART2,USART_FLAG_TC) != SET);
}
void USART2_WriteBytes(uint8_t n, uint8_t *p)
{
	uint8_t i;
	for(i=0;i<n;i++)
	{
		USART2_WriteByte(p[i]);
	}
}

void USART2_Init(u32 baud)
{
   //GPIO端口设置
	GPIO_InitTypeDef GPIO_InitStructure;
	USART_InitTypeDef USART_InitStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2,ENABLE);
 
	
	/*  配置GPIO的模式和IO口 */
	GPIO_InitStructure.GPIO_Pin=GPIO_Pin_2;//TX			   //串口输出PA2
	GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Mode=GPIO_Mode_AF_PP;	    //复用推挽输出
	GPIO_Init(GPIOA,&GPIO_InitStructure);  /* 初始化串口输入IO */
	GPIO_InitStructure.GPIO_Pin=GPIO_Pin_3;//RX			 //串口输入PA3
	GPIO_InitStructure.GPIO_Mode=GPIO_Mode_IN_FLOATING;		  //模拟输入
	GPIO_Init(GPIOA,&GPIO_InitStructure); /* 初始化GPIO */
	

   //USART2 初始化设置
	USART_InitStructure.USART_BaudRate = baud;//波特率设置
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;//字长为8位数据格式
	USART_InitStructure.USART_StopBits = USART_StopBits_1;//一个停止位
	USART_InitStructure.USART_Parity = USART_Parity_No;//无奇偶校验位
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//无硬件数据流控制
	USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;	//收发模式
	USART_Init(USART2, &USART_InitStructure); //初始化串口2
	
	USART_Cmd(USART2, ENABLE);  //使能串口2 
	
	USART_ClearFlag(USART2, USART_FLAG_TC);
		
	USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);//开启相关中断

	//Usart1 NVIC 配置
	NVIC_InitStructure.NVIC_IRQChannel = USART2_IRQn;//串口2中断通道
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=3;//抢占优先级3
	NVIC_InitStructure.NVIC_IRQChannelSubPriority =2;		//子优先级3
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;			//IRQ通道使能
	NVIC_Init(&NVIC_InitStructure);	//根据指定的参数初始化VIC寄存器、	
}

/*******************************************************************************
* 函 数 名         : USART2_IRQHandler
* 函数功能		   : USART2中断函数
* 输    入         : 无
* 输    出         : 无
*******************************************************************************/ 
void USART2_IRQHandler(void)                	//串口2中断服务程序
{
	if(USART_GetITStatus(USART2, USART_IT_RXNE) != RESET)  //接收中断
	{
		if(!USART2_QUEUE_FULL())
        {
//            USART2_PUSH_QUEUE(USART_ReceiveData(USART2));
			if(USART_ReceiveData(USART2)==0xa9)
			{
				ADC_CLEAR_QUEUE();
				TIM_Cmd(TIM4,ENABLE); //使能定时器	
			}
			if(USART_ReceiveData(USART2)==0xb9)
			{
				TIM_Cmd(TIM4,DISABLE); //关闭定时器	
			}
			
        }
	} 
	USART_ClearFlag(USART2,USART_FLAG_TC);
} 	
