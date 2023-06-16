# Đồ án thực tập chuyên ngành: Dự đoán tuổi thông qua khuôn mặt
***
## Thông tin đề tài:
-  Giáo viên hướng dẫn:   TS. Nguyễn Tuấn Linh
-  Họ và tên:                     Phạm Sỹ Quang
-  Lớp:                                               55KMT
-  MSSV:                           K195480106018
***
> Cài đặt chương trình [Click vào đây để có thể tải và cài đặt](https://drive.google.com/file/d/1qQSO8CZqYydPYnCKvk3nby5fDRqUsrkD/view?usp=sharing)
## Thông tin về đề tài
### Nội dung đề tài:
* Thông qua kiến thức đã học được để xây dựng một chương trình dự đoán tuổi thông qua khuôn mặt
* Sử dụng thuật toán CNN để có thể nhận diện tuổi
* Xây dựng ứng dụng độc lập thông qua ứng dụng chạy trên nền tảng Windows
### Phân tích dữ liệu và huấn luyện
* Dữ liệu được lấy từ bộ dữ liệu trên UTK Faces: [Tải bộ dữ liệu](https://susanqq.github.io/UTKFace/)
* Dữ liệu bao gồm có 32,683 bức ảnh với độ tuổi, giới tính, dân tộc khác nhau

                                               ![Ảnh dữ liệu](https://i.imgur.com/X1H0EEQ.png)
* Dữ liệu bao gồm các độ tuổi từ 1 -> 100 tuổi

                                               ![Ảnh dữ liệu](https://i.imgur.com/iMK8GNp.png)
* Sau khi đã loại bỏ những thông tin không cần thiết trong quá trình huấn luyện, kết quả đã thu được dữ liệu chuẩn bị huấn luyện như sau:

                                                     ![Ảnh thông tin dũ liệu](https://i.imgur.com/fGBNjWt.png)
* Thực hiện chia khoảng độ tuổi

                                               ![Ảnh dữ liệu](https://i.imgur.com/WlAYJeA.png)
* Thực hiện huấn luyện mô hình

                                                        ![Kiến trúc mô hình](https://i.imgur.com/qh5yqhN.png)
* Kết quả huấn luyện mô hình

                                               ![Kết quả huấn luyện mô hình](https://i.imgur.com/vR3ggoB.png)
### Thực hiện kiểm thử và xây dựng chương trình phần mềm
* Chương trình kiểm thử dữ liệu dưới dạng ảnh

                                                   ![Kiểm thử dữ liệu ảnh](https://i.imgur.com/Iv117oY.png)
* Chương trình kiểm thử dữ liệu dưới lấy trực tiếp từ Camera

                                         ![Kiểm thử dữ liệu lấy từ Camera](https://i.imgur.com/YmfnM2E.png)
* Xây dựng phần mềm

                                                        ![Xây dựng phần mềm](https://i.imgur.com/Gw2p8N8.png)
