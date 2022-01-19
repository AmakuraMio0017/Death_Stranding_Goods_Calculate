resource_initial = (40,50,40,60,30)
name_of_resource = ('树脂','金属','陶瓷','特殊合金','化学品')
#五种资源在提取时拥有7个不同的提取梯度，这是最小的提取单位和资源名称，用来计算之后的梯度列表

def calculate_delta_M():                    #计算delta_M，无调用，打印所需资源，返回delta_M
    while True:
        all_M = int(input('请输入建造点所需要的总资源量:'))
        now_M = int(input('请输入建造点已经拥有的资源量:'))
        if isinstance(all_M,int) and isinstance(now_M,int) and all_M > now_M :
            break
        else:
            print('请输入正确的数值')
    delta_M = all_M - now_M
    print('则，参与计算 ΔM = ' + str(delta_M))
    return delta_M

def number_of_step(type_of_resource):       #计算梯度列表，无调用，打印梯度列表，返回resource_list
    #number_of_step()函数用于根据给定的资源特征参数“type_of_resource”列出全部所需资源梯度表
    k_order_1 = resource_initial[type_of_resource]
    print('您希望提取的是' + name_of_resource[type_of_resource] + '，其最小携带单位为' + str(k_order_1))
    resource_list = [k_order_1]
    for i in [2,3,4]:
        resource_list.append(k_order_1 * 2 ** (i - 1))
    for i in [5,6,7]:
        resource_list.append(k_order_1 * 8 + k_order_1 * 4 * (i - 4))
    print(name_of_resource[type_of_resource] + '的可提取梯度列表为' + str(resource_list))
    return resource_list

def position(delta_M):                      #计算delta_M位置，调用number_of_step，返回position_code
    #position()函数用于确定ΔM同number_of_step()函数给定列表的相对位置关系
    #   (list1) (list2) (list3) ……
    #   i=0     i=1     i=2     ……
    if delta_M < list[0]:       #若所需资源量（ΔM）小于“number_of_step函数返回列表”的最小值
        position_code = 'min'   #返回“位置特征码”:'min'
    elif delta_M > list[6]:     #若所需资源量（ΔM）大于“number_of_step函数返回列表”的最大值
        position_code = 'max'   #返回“位置特征码”:'max'
    else:                       #若所需资源量（ΔM）正好符合“number_of_step函数返回列表”中的某一个值
        for i in range(7):      #遍历list[0-6]寻找，所需数值只可能是介于“number_of_step函数返回列表”最大、最小值之间，或者等于其中某个特定值
            if delta_M - list[i] <= 0:
                break
        position_code = i       #返回“位置特征码”: i
    return position_code        #仅有可能返回'min'、'max'和i，i的值应在0-6之间

def count_if_middle(p , q , delta_M , i):   #计算All包用量，调用number_of_step，返回list_out
    list_out = [p]
    while i > 0:
        i -= 1
        p = q // list[i]
        q = q % list[i]
        if p == 0 and q != 0:       #新模=0，新余≠0时
            if i != 0:
                list_out.append(0)
                continue
            else:
                list_out.append(0)  #模=0，余≠0，但序数已到最后，最后一组+1
                a = list_out.pop()
                list_out.append(int(a) + 1)
                break
        elif p != 0 and q != 0:     #新模≠0，新余≠0时
            if i != 0:
                list_out.append(p)
                continue
            else:
                list_out.append(p)  #模≠0，余≠0，但序数已到最后，最后一组+1
                a = list_out.pop()
                list_out.append(int(a) + 1)
                break
        elif p == 0 and q == 0:
            list_out.append(0)
            continue
        elif p != 0 and q == 0:     #新模≠0，新余=0时
            list_out.append(p)
            continue
    return list_out

def count_if_max(delta_M):                  #计算Max、All包用量，调用number_of_step、count_if_middle，打印包用量，返回None
    i = 6   
    p = delta_M // list[i]
    list_out = [p]
    q = delta_M % list[i]
    if q == 0:
        print('需要最大号，' + str(list[6]) + '单位资源' + str(p) + '个整')
    else:
        list_out = count_if_middle(p , q , delta_M , i)
        list_out.reverse()
        all = 0
        for k in range(7):
            print("{}{}{}{}{}{}".format(k + 1,".需要提取",list[k],"资源包",list_out[k],"个"))
            all_re = list[k] ; all_mo = list_out[k]
            all += all_re * all_mo
        waste = all - delta_M
        print("{}{}{}{}".format("共计提取:",all,"\n损失:",waste))

def needs_list_printer(delta_M , po):       #嵌套函数，调用position、number_of_step、count_if_max、count_if_middle，打印包用量，返回None
    if po == 'min':
        print('仅需要' + str(list[0]) + '单位资源一个')
        waste = list[0] - delta_M
        print("{}{}".format("损失:",waste))
    elif po == 'max':
        count_if_max(delta_M)
    else:
        po = int(po) - 1
        p = delta_M // list[po]
        q = delta_M % list[po]
        list_out = count_if_middle(p , q , delta_M , po)
        list_out.reverse()
        list_out.extend([0] * (7 - po))
        all = 0
        for k in range(7):
            print("{}{}{}{}{}{}".format(k + 1,".需要提取",list[k],"资源包",list_out[k],"个"))
            all_re = list[k] ; all_mo = list_out[k]
            all += all_re * all_mo
        waste = all - delta_M
        print("{}{}{}{}".format("共计提取:",all,"\n损失:",waste))


print('欢迎使用《死亡搁浅》资源提取计算器\n======================================================')
while True:
    type_of_resource = input('请输入:0.树脂 1.金属 2.陶瓷 3.特殊合金 4.化学品 5.退出\n')
    if type_of_resource in ['0','1','2','3','4']:
        type_of_resource = int(type_of_resource)
        list = number_of_step(type_of_resource)
        delta_M = calculate_delta_M()
        po = position(delta_M)
        needs_list_printer(delta_M , po)
        print('======================================================')
    elif type_of_resource == '5':
        break
    else:
        print('请输入0-5的整数')