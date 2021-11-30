50# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 20:12:59 2021

@author: dongh

Target: tạo ra một bộ dữ liệu để áp dụng cho thuật toán với đặc trưng của cơ sở dữ liệu phân tán
Tức là số item là khoảng 10.000 - 100.000
Số node (cơ sở dữ liệu địa phương) là khoảng 100-2.000 
Phân phối dữ liệu:
    - Phân phối Zipf
    - Phân phối uniform (phân phối đều)
    - Phân phối Gauss (phân phối norm/phân phối chuẩn)

"""

# nhap thu vien
import numpy as np
from numpy.lib.function_base import sort_complex


print ("Lặp lại 4 bước bên dưới c lần. Nhập c: ")
c = int(input())

#chuyển mảng 2 chiều sang 1 chiều ('list of list' _to_ 'list'):
#vd: [[1,2,3],[4,5,6]] => [1,2,3,4,5,6]
def convert2dto1d(arr2d):
    arr1d = []
    for item in arr2d:
        for j in range (len(item)):
            arr1d.append (item[j])
    return arr1d

#trung tâm xử lý dữ liệu ở bước 3, với các cặp có cùng id thì giữ lại 1 cặp có giá trị Rij nhỏ nhất
def center_process(tup_list):
    # 1 list để lưu key
    list_key= []

    # 1 list để lưu các pairs tạm thời có cùng key
    # 1 list target 
    list_target = []

    for item in tup_list:
        if item[0] not in list_key:
            list_key.append(item[0])

    for key in list_key:
        list_temp = []

        for item in tup_list:
            if item[0] == key:
                list_temp.append(item)
        list_temp.sort()
        list_target.append(list_temp[0])

    print("Sau bước 3: node_score: ",list_target)
    print("\n")
    return list_target

#giữ lại N phần tử nhỏ nhất trong list
def get_some_couple(arr, n):
    # xóa các phần tử không nằm trong N phần tử nhỏ nhất: (tổng - N) phần tử ở cuối list
    i = len(arr)
    while (i > n):
        i-=1
        arr.pop()
    print("\n",n," cặp được chọn/gửi đi:",arr)
    print("\n")
    return arr

def accuracy(arr,k):
        score = 0
        for i in arr:
            if i <= k:
                score += 1
        return score/len(arr)*100

#in ra k phần tử có số lần lặp lại nhiều nhất trong mảng: arr (arr có n phần tử)
def find_top_K_occurrences(arr, n, k):
    um = {}
    for i in range(n):
        if arr[i] in um:
            um[arr[i]] += 1
        else:
            um[arr[i]] = 1
    a = [0] * (len(um))
    j = 0
    for i in um:
        a[j] = [i, um[i]]
        j += 1
    a = sorted(a, key=lambda x: x[0],
               reverse=False)
  
    # display the top k numbers
    temp = []

    print(k, "mục là kết quả của bài toán tìm kiếm top K:")
    for i in range(k):
        print("item",a[i][0], end="\n")
        temp.append(a[i][0])
    return temp
    
    


# BƯỚC 1: Khởi tạo bộ dữ liệu:
# mỗi cột sẽ sinh bộ dữ liệu gồm n phần tử, lặp lại m lần như vậy 
# kết quả thu được là 1 bảng giá trị gồm n hàng và m cột 
# (tất cả các phần tử trong mảng - điểm đánh giá của mỗi item trên mỗi node, đều được sinh ngẫu nhiên)
# việc của chúng ta là tìm ra k hàng có tổng lớn nhất (k items có điểm đánh giá cao nhất)

    ##### DIỄN GIẢI ######
    # cách trâu bò nhất để ra được kết quả bài toán (mà không áp dụng thuật toán top K) là:
    #1: Tính tổng từng hàng 
    #2: Tìm k hàng có tổng lớn nhất
    #3: Lấy số thứ tự của k hàng đó và in ra màn hình (đó là kết quả)

    # cách theo thuật toán top K:
    #1: Gán id cho mỗi phần tử trong mảng node_score 
        # (vì bước sau thứ tự các phần tử trong mỗi cột sẽ bị xáo trộn nên phải gán id để biết được lúc đầu,
        # phần tử đó thuộc hàng nào - id chính là số thứ tự hàng của phần tử ban đầu)
        # gán bằng cách nào?
            # bình thường kiểu dữ liệu của phần tử sau khi sinh ngẫu nhiên bằng hàm random() sẽ chỉ lưu được
            # 1 giá trị. Bây giờ sẽ dùng phương pháp để thay đổi kiểu dữ liệu của phần tử đó sang kiểu "tuple".
            # Cuối cùng, duyệt đến từng phần tử, gán phần tử cũ (kiểu dữ liệu cũ) bằng phần tử mới (kiểu
            # dữ liệu "tuple"), khi đó mỗi phần tử mới có dạng: "(i: Rij)" 
                # với i là id của phần tử (tượng trưng cho phần tử đó là mảnh của items nào)
                # và Rij là giá trị của phần tử (tức là mảnh đó có giá trị là bao nhiêu)
                # Ví dụ 1 phần tử "node_score[4,37] = tuple: (6,2.08449267)" sẽ biểu thị đó là 
                    # mảnh của items 6 (vì có id = 6), mảnh đó nằm ở cơ sở dữ liệu thứ 37, có giá trị R(6,37) = 2.08449267
                    # và vị trí hiện tại của mảnh này đang nằm ở hàng 4, cột 37. Vị trí ban đầu chưa sắp xếp ở hàng 6, cột 37
    #2: Chọn ra k cặp (i, Rij) có Rij nhỏ nhất (với i không trùng nhau); giữ lại chỉ số thôi
        # ví dụ chọn được 2 cặp là [(3, 6.8503),(5, 9.463542),(8, 7.9086)] thì biến nó thành [3,5,8]

    #3: Lặp lại việc sinh giá trị ngẫu nhiên cho mảng node_score (#BƯỚC 1), rồi bước #1, rồi bước #2 vài lần
        # (ở đây là 'c' lần với c là số tự nhiên do user nhập)
        # thì ở các lần khác nhau, số liệu khác nhau dẫn đến k cặp xuất hiện ở bước #2 sẽ khác nhau.
        # tức là kết hợp lại, các kết quả ở bước #2 sẽ nhiều lên và lớn hơn k.
        # thì cuối cùng, 
            # chọn ra k cặp (i, Rij) trong tập hợp các cặp được sinh ra sau c lần lặp lại đó; 
            # điều kiện là k cặp này có chỉ số i lặp lại nhiều nhất.
            # ví dụ như [3,5,8] trên kia nhá, giờ cho c = 3 đi, thì nó chạy 3 lần (giả sử phải chọn ra k = 3 cặp đi):
                #Lần 1 được [3,5,8]
                #Lần 2 được [3,6,8]
                #Lần 3 được [2,6,3]
                #Tổng kết lại thấy 
                    #[3] lặp lại 3 lần, 
                    #[8] lặp lại 2 lần,
                    #[6] lặp lại 2 lần,
                    #[2] lặp lại 1 lần,
                    #[5] lặp lại 1 lần. Suy ra lấy k=3 items lặp lại nhiều nhất thì kết quả là:
                        # Item 3, Item 8, Item 6

    ####### Kết thúc phần DIỄN GIẢI #########

    ##### BẮT ĐẦU ###########

m = 20
n = 100 

res_all_time = [] #tổng hợp kết quả sau c lần lặp
res_final = [] #kết quả cuối cùng của bài toán (sẽ là k giá trị có số lần lặp lại 
                #nhiều nhất nằm trong list 'res_all_time')


item_score = np.random.zipf(2, size= n) 
item_score = np.sort(item_score)
print("item_score_debug: ",item_score)
delay = input()

#yêu cầu user nhập k hoặc để máy tự nhập
print("Nhập k (giữ lại k cặp): ")
k = int(input())
# k = int(n*0.1)

# yêu cầu user nhập hằng số N hoặc để máy tự nhập 
print("Nhap hang so N: ")
N = int(input())
# N = m*n/2
print("\n")


for iter in range (c): # Lặp lại c lần tất cả các bước
    print("Lặp lại 4 bước lần thứ ",iter+1)

#BƯỚC 1: Sinh bộ dữ liệu
    # sinh các item
    #tạo 2D list để lưu phân mảnh tất cả mỗi item trong n item ra m node
    node_score = [[0 for i in range(m)] for j in range(n)] 

    for i in range(n):
        temp = np.random.uniform(0, 10, m) # m phần này phân phối đều
        t = np.sum(temp)

        for j in range(m):
            node_score[i][j] = (n-i, item_score[i]*(temp[j]/t))

    print("Sau bước 1: node_score: ",node_score)
    print("\n")


#BƯỚC 2: Sắp xếp các cặp theo Rij tại mỗi node, gửi N cặp có Rij nhỏ nhất về trung tâm xử lý.

    # chuyển từ mảng 2 chiều sang 1 chiều (gộp m list con (mỗi list n phần tử) trong 1 list to thành 1 list m*n phần tử)
    node_score = convert2dto1d(node_score)

    # sắp xếp mảng 1 chiều: (theo Rij)
    node_score.sort(key=lambda x:x[1])
    print("node_score_debug: ",node_score)


    # lấy N phần tử gửi về trung tâm xử lý
    node_score = get_some_couple(node_score,N)


#BƯỚC 3: Trung tâm xử lý N cặp gửi về (lấy cặp có Rij nhỏ nhất trong các cặp có i trùng nhau)
        # ví dụ có 3 cặp (3, 7.54643),(3, 5.45346),(3, 2.342564) thì lấy cặp (3,2.342564); còn 2 cặp còn lại xóa đi
    node_score = center_process(node_score)

#BƯỚC 4: 
        #giữ lại k cặp có Rij nhỏ nhất trong node_score:
    node_score = get_some_couple(node_score,k)

        #lấy chỉ số của k cặp được giữ lại tương đương với kết quả cuối cùng của từng lần (mỗi lần là 4 bước trên)
    res_each_time = []
    for key,val in node_score:
        res_each_time.append(key)

    res_all_time.append(res_each_time)

#TÌM KẾT QUẢ CUỐI CÙNG:
res_all_time = convert2dto1d(res_all_time)
list_result = find_top_K_occurrences(res_all_time,len(res_all_time),k)
print("Độ chính xác: ", "{:.2f}".format(accuracy(list_result,len(list_result))),"%")