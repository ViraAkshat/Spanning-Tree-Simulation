from bridge import Bridge, Lan, Network

def torder(t):
    return t[0]

def parser_input(inp):
    return [inp.split(":")[0]]+inp.split(":")[1].split(" ")[1:]

if __name__ == '__main__':
    flag_input = (input()=='1')
    bridges_count = int(input())

    net = Network()
    bridges_dict = {}
    lans_dict = {}

##########################################################################################
    #  Reading Inputs

    for i in range(0,bridges_count):
        bridge_inputs = parser_input(input().strip("\r\n"))
        if len(bridge_inputs)>1:
            net.add_bridge(Bridge(bridge_inputs[0]))
            for j in range(1,len(bridge_inputs)):
                net.add_port(bridge_inputs[j].strip(" \r\n"),bridge_inputs[0])
                if bridge_inputs[j].strip(" \r\n")!="":
                    lans_dict[bridge_inputs[j]] = []

    for i in range(len(lans_dict.keys())):
        lan_inputs = parser_input(input())

        if lan_inputs[0] not in lans_dict.keys():
            print("error1: Wrong input format",lan_inputs[0],lans_dict)

        if len(lan_inputs)>1:
            for j in range(1,len(lan_inputs)):
                net.add_host(lan_inputs[j],lan_inputs[0])
        
    flag = 0
    if flag_input:
        flag = 1

    t = 0
    trace = []
#########################################################################################
    # Spanning Tree Protocol Simulation

    while net.update:

        net.update = False
        
        for bridge in net.bridges:
            net.bridges[bridge].send_msg(t)

            for lan in net.bridges[bridge].lans:
                net.bridges[bridge].lans[lan][0].send_msg()
                net.bridges[bridge].lans[lan][0].update()

            net.bridges[bridge].update()
            trace.append(net.bridges[bridge].trace)
            
        t += 1
        net.change()
        
    for bridge in net.bridges:
        net.bridges[bridge].null_port()
#########################################################################################
    # Reading Input for Packet Transmission

    transmit_count = int(input())
    transmit_ip = []
    for l in range(transmit_count):
        transmit = input().split()
        if len(transmit)!=2:
            print('error2: Wrong input format')
            exit(0)
        transmit_ip.append(transmit)

    if(flag):
        for t in trace:
            t.sort(key=torder)
            print(t)

    bridge_output = {}

    for bridge in net.bridges:
        for lan in net.bridges[bridge].lans:
            z = net.bridges[bridge].port(lan)
            if z[0] not in bridge_output.keys():
                bridge_output[z[0]]=[z[1]+'-'+z[2]]
            else:
                bridge_output[z[0]].append(z[1]+'-'+z[2])
######################################################################
    # Printing Bridge Status Output 

    b_str = ''
    for k in bridge_output.keys():
        b_str = f'{k}:' #.format(k)

        p_list = []
        for m in sorted(bridge_output[k]):
            b_str = b_str + f' {m}' #.format(m)

        print(b_str)

    transmit_op = []

    for l in range(transmit_count):

        transmit_op_list = []
        transmit = transmit_ip[l]
        if len(transmit)!=2:
            print('error2: Wrong input format')
            exit(0)

######################################################################
        # Host to Host Packet Transfer

        net.transmit(transmit[0],transmit[1])

######################################################################
    # Printing Bridge Forwarding Table

        t_str = ''
        for bridge in net.bridges:

            transmit_op_list.append(f'{bridge}:')
            transmit_op_list.append('HOST ID | FORWARDING PORT')

            t_op = net.bridges[bridge].forward
            t_op_list_sorted = sorted(t_op.items())
            t_l = []

            for t in t_op_list_sorted:
                t_l.append(f'{t[0]} | {t[1]}')
            transmit_op_list.append('\n'.join(t_l))

        transmit_op.append('\n'.join(transmit_op_list))

    print('\n\n'.join(transmit_op))

        
