#include "usart1.h"
#include "adc.h"
uint8_t USART1_RECEIEVE_QUEUE_BUF[USART1_MAX_QUEUE_BUF_SIZE];//USART1串口缓冲区
uint8_t USART1_QUEUE_REAR=0;//串口缓冲区队列尾，入队位置
uint8_t USART1_QUEUE_FRONT=0;//串口缓冲区队列首，出队位置
/**
  * @brief :判断USART1串口缓冲区是否满
  * @param :void
  * @retval :返回1:满 返回0:非满
  * @usage:if(USART1_QUEUE_FULL()==1)...	if(USART1_QUEUE_FULL()==0)...
  */
uint8_t  USART1_QUEUE_FULL(void)
{
    return (uint8_t)(((USART1_QUEUE_REAR+1)% USART1_MAX_QUEUE_BUF_SIZE)==USART1_QUEUE_FRONT);
}


/**
  * @brief	:判断USART1串口缓冲区是否空
  * @param	:void
  * @retval	:返回1:空 返回0:非空
  * @usage	:if(USART1_QUEUE_EMPTY()==1)...	if(USART1_QUEUE_EMPTY()==0)...
  */
uint8_t USART1_QUEUE_EMPTY(void)
{
    return (uint8_t)(USART1_QUEUE_REAR==USART1_QUEUE_FRONT);
}

/**
  * @brief	:往USART1串口缓冲区内存入一个字节数据
  * @param	ch: uint8_t类型，写入ch
  * @retval	:1,队列满，写入失败；0，写入成功
  * @usage	:USART1_PUSH_QUEUE(0x3f)
  */
uint8_t USART1_PUSH_QUEUE(uint8_t ch)
{
    if(USART1_QUEUE_FULL())
    {
        printf("queue full!\n");
        return 1;
    }
    USART1_QUEUE_REAR=(USART1_QUEUE_REAR+1) % USART1_MAX_QUEUE_BUF_SIZE;
    USART1_RECEIEVE_QUEUE_BUF[USART1_QUEUE_REAR]=ch;
    return 0;
}
/**
  * @brief	:从USART1串口缓冲区取出一个字节数据
  * @param	:void
  * @retval	:uint8_t 类型，即为从缓冲区取出的字节
  * @usage	:uint8_t temp;
  * @usage	:temp=USART1_POP_QUEUE();
  */
uint8_t USART1_POP_QUEUE(void)
{
    uint8_t temp;
    if(USART1_QUEUE_EMPTY())
    {
        printf("queue empty!\n");
        return 1;
    }
    USART1_QUEUE_FRONT = (USART1_QUEUE_FRONT+1)%USART1_MAX_QUEUE_BUF_SIZE;
    temp = USART1_RECEIEVE_QUEUE_BUF[USART1_QUEUE_FRONT];
    return temp;
}
int fputc(int ch, FILE *p)
{
	USART_SendData(USART1,(u8)ch);
	while(USART_GetFlagStatus(USART1,USART_FLAG_TC) != SET);
	return ch;
}

void USART1_WriteByte(uint8_t ch)
{
	USART_SendData(USART1,(u8)ch);
	while(USART_GetFlagStatus(USART1,USART_FLAG_TC) != SET);
}
void USART1_WriteBytes(uint8_t n, uint8_t *p)
{
	uint8_t i;
	for(i=0;i<n;i++)
	{
		USART1_WriteByte(p[i]);
	}
}

void USART1_Init(u32 baud)
{
   //GPIO端口设置
	GPIO_InitTypeDef GPIO_InitStructure;
	USART_InitTypeDef USART_InitStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1,ENABLE);
 
	
	/*  配置GPIO的模式和IO口 */
	GPIO_InitStructure.GPIO_Pin=GPIO_Pin_9;//TX			   //串口输出PA9
	GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Mode=GPIO_Mode_AF_PP;	    //复用推挽输出
	GPIO_Init(GPIOA,&GPIO_InitStructure);  /* 初始化串口输入IO */
	GPIO_InitStructure.GPIO_Pin=GPIO_Pin_10;//RX			 //串口输入PA10
	GPIO_InitStructure.GPIO_Mode=GPIO_Mode_IN_FLOATING;		  //模拟输入
	GPIO_Init(GPIOA,&GPIO_InitStructure); /* 初始化GPIO */
	

   //USART1 初始化设置
	USART_InitStructure.USART_BaudRate = baud;//波特率设置
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;//字长为8位数据格式
	USART_InitStructure.USART_StopBits = USART_StopBits_1;//一个停止位
	USART_InitStructure.USART_Parity = USART_Parity_No;//无奇偶校验位
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//无硬件数据流控制
	USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;	//收发模式
	USART_Init(USART1, &USART_InitStructure); //初始化串口1
	
	USART_Cmd(USART1, ENABLE);  //使能串口1 
	
	USART_ClearFlag(USART1, USART_FLAG_TC);
		
	USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);//开启相关中断

	//Usart1 NVIC 配置
	NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;//串口1中断通道
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=3;//抢占优先级3
	NVIC_InitStructure.NVIC_IRQChannelSubPriority =3;		//子优先级3
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;			//IRQ通道使能
	NVIC_Init(&NVIC_InitStructure);	//根据指定的参数初始化VIC寄存器、	
}

/*******************************************************************************
* 函 数 名         : USART1_IRQHandler
* 函数功能		   : USART1中断函数
* 输    入         : 无
* 输    出         : 无
*******************************************************************************/ 
void USART1_IRQHandler(void)                	//串口1中断服务程序
{
	if(USART_GetITStatus(USART1, USART_IT_RXNE) != RESET)  //接收中断
	{
		if(!USART1_QUEUE_FULL())
        {
//            USART1_PUSH_QUEUE(USART_ReceiveData(USART1));
			if(USART_ReceiveData(USART1)==0xa9)
			{
				ADC_CLEAR_QUEUE();
				TIM_Cmd(TIM4,ENABLE); //使能定时器	
			}
			if(USART_ReceiveData(USART1)==0xb9)
			{
				TIM_Cmd(TIM4,DISABLE); //关闭定时器	
			}
			
        }
	} 
	USART_ClearFlag(USART1,USART_FLAG_TC);
} 	
