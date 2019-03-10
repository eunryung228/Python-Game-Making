ans_r1=[0,1,0,1,0,1,0,1,0,1,1,0,0,0,1,0,1,0,1,0,0,0,1,0,0]
ans_r2=[0,0,0,1,1,1,1,0,0,1, 1,0,1,0,0,0,0,1,0,0, 0,0,1,1,0,1,0,1,0,0,
        0,0,1,0,0,0,0,1,0,0, 1,0,0,1,1,1,1,0,0,1, 0,0,1,0,0,0,0,1,0,0,
        0,1,0,0,0,0,0,0,1,0, 0,1,0,0,1,1,0,0,1,0, 0,1,0,0,0,0,0,0,1,0, 0,0,1,1,1,1,1,1,0,0]
ans_r3=[0,0,0,0,0,1,1,0,0,1, 0,0,0,0,0,0,1,0,1,0, 0,0,0,1,0,1,1,1,0,0,
        0,0,1,0,1,1,1,1,1,1, 0,0,0,1,0,1,1,1,0,1, 1,0,1,1,1,0,1,0,0,0,
        1,1,1,1,1,1,0,0,0,0, 0,0,1,1,1,0,0,0,0,0, 0,1,0,1,0,0,0,0,0,0, 1,0,0,1,1,0,0,0,0,0]
ans_r4=([0]*20+[0,0]+[1]*16+[0,0]+[1]*3+[0]*14+[1]*3+[1,0,1]+[1,0]*7+[1,0,1]+[1,0,1]+[0]*14+[1,0,1])+\
       ([1,0,1]+[0]*3+[1,0,1,0,0,1,0,1]+[0]*3+[1,0,1]+[1,0,1]+[0]*2+[1,0,1,0,1,1,0,1,0,1]+[0]*2+[1,0,1]+[0,1,1]+[0]*3+[1,0,1,0,0,1,0,1]+[0]*3+[1,1,0])+\
       ([0,0,1]+[0]*4+[1,0,1,1,0,1]+[0]*4+[1,0,0]+[0,0,0,1]+[0]*4+[1]*4+[0]*4+[1,0,0,0]+[0,0,0,1]+[0]*12+[1,0,0,0])+\
       ([0,1,0,0,1]+[0]*10+[1]+[0]*4+[1,0,1,0,0,1]+[0]*8+[1,0,0,1,0,0]+[0,1]+[0]*4+[1]*8+[0,0,1,0,1,0]+[0]*7+[1]+[0]*4+[1]+[0]*4+[1,0,0])+\
       ([0]*3+[1]+[0]*4+[1,0,0,1]+[0]*8+[0,0]+[1]*3+[0]*3+[1,0,1,1]+[0]*6+[1,0]+[0]*3+[1,0,0,1,1,0,0]+[1]*4+[0]*3+[1]*3)+\
       ([0,1,0,0,0,1,1,0,0]+[1]*6+[0]*3+[1,0]+[1,0,1,0]+[1]*12+[0]*4)
# 정답표

def get_ans(n, r): # 해당 칸이 1이면(색칠해야 되는 칸이면) True를 리턴, 아니면 False를 리턴
    if r==1: return ans_r1[n]
    elif r==2: return ans_r2[n]
    elif r==3: return ans_r3[n]
    elif r==4: return ans_r4[n]

def check_clear(n, r): # 각 round마다 포함된 1의 개수를 세서 현재 클릭한 총 칸의 개수와 같으면 round를 clear한 것이므로 True를 리턴
    if r==1:
        if n == ans_r1.count(1): return True
        else: return False
    elif r==2:
        if n==ans_r2.count(1): return True
        else: return False
    elif r==3:
        if n==ans_r3.count(1): return True
        else: return False
    elif r==4:
        if n==ans_r4.count(1): return True
        else: return False

def get_row_col(r, anslist): # 각 board에 대한 rowlist와 collist를 리턴
    if r == 1: l_num = 5
    elif r==2 or r==3: l_num = 10
    elif r==4: l_num=20
    row = []; col = []
    for i in range(l_num):
        row.append(anslist[i*l_num:i*l_num+l_num])
        list = []
        for j in range(l_num):
            list.append(anslist[i+j*l_num])
        col.append(list)
    return row, col

def get_numlist(r): # rowlist와 collist에 각각 포함된 1의 개수를 받음
    if r==1:
        l_num=5
        row, col=get_row_col(r, ans_r1)
    elif r==2:
        l_num=10
        row, col=get_row_col(r, ans_r2)
    elif r==3:
        l_num=10
        row, col=get_row_col(r, ans_r3)
    elif r==4:
        l_num=20
        row, col=get_row_col(r, ans_r4)
    # 먼저 row와 col을 생성함

    r_count=0; c_count=0; r_list=[]; c_list=[]; rowlist=[]; collist=[]
    for i in range(l_num):
        for j in range(l_num):
            if row[i][j]==1: # 해당 칸이 1이면
                r_count+=1   # count+=1
                if j == l_num-1: # 해당 줄의 마지막 칸이면
                    r_list.append(r_count)  # r_list에 지금까지 센 r_count 추가
                    r_count = 0 # 초기화
            elif row[i][j] == 0 and r_count > 0: # 0을 만났는데 r_count가 0보다 크면
                r_list.append(r_count) # r_list에 지금까지 센 r_count 추가
                r_count = 0 # 초기화
            # row에 대한 계산

            if col[i][j] == 1:
                c_count += 1
                if j == l_num-1:
                    c_list.append(c_count)
                    c_count = 0
            elif col[i][j] == 0 and c_count > 0:
                c_list.append(c_count)
                c_count = 0
            # col에 대한 계산, row와 같은 방식

        rowlist.append(r_list) # rowlist에 각 줄에 대한 r_list를 추가
        r_list=[]
        collist.append(c_list) # collist에 각 줄에 대한 c_list를 추가
        c_list=[]
    if r==4: rowlist[0]=[0]    # 마지막 라운드의 첫 행은 색칠할 칸이 하나도 없는데, 이 경우가 한 가지 경우밖에 없어서 예외처리 해줌
    return rowlist, collist