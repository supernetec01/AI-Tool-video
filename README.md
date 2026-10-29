# Mẹ Bỉm Thông Thái — Dinh dưỡng mẹ bầu, Tập 01

Video tiếng Việt về **5 thực phẩm hỗ trợ phát triển não bộ thai nhi**, dựng bằng Remotion và video-shotcraft. Thời lượng 60 giây, khung dọc 1080 × 1920, 24 fps; hình ảnh AI có chuyển động nhẹ, màu kem–hồng đào.

## Thành phẩm

- [Video có nhạc piano](deliverables/mombite-01.mp4)
- [Video không nhạc, giữ âm chuyển cảnh](deliverables/mombite-01-khong-nhac.mp4)
- [Dự án Jianying Desktop](deliverables/MomBite01-Jianying.zip) — 8 cảnh, 52 đoạn chữ native, nhạc và hiệu ứng âm thanh riêng.
- [Lời thoại](deliverables/loi-thoai.txt), [phụ đề SRT](deliverables/mombite-01.vi.srt), [ảnh bìa](deliverables/anh-bia.png).

Bản dựng hiện **chưa có giọng đọc**. SRT là kịch bản để lồng tiếng/chỉnh sửa, không phải bản chép lời của âm thanh đã có. Ảnh là minh họa AI, không phải footage quay thật; có nhãn nhận diện trong video.

## Cài đặt và dựng lại

Quy trình dựng đã kiểm tra trên Linux với Node 24, Python 3.12, FFmpeg và Chromium tại `/usr/bin/chromium`. Dùng checkout hiện tại; không cần tạo Git worktree.

```bash
npm ci
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
npm run check
npm run dev
```

Các ảnh, font và âm thanh cần thiết đã nằm trong `public/`, không cần API key.

```bash
# Tùy chọn: tạo lại bản nhạc và âm chuyển cảnh từ mã nguồn.
.venv/bin/python scripts/make-audio.py

# Xuất hai bản video; kết quả và các khung kiểm tra nằm trong out/.
npm run render

# Nếu đã có out/mombite-01.mp4, có thể tạo bản không nhạc mà không dựng lại hình:
node scripts/render-nomusic.mjs
```

## Xuất dự án Jianying

Để dùng ngay: giải nén [gói dự án](deliverables/MomBite01-Jianying.zip), đọc `HUONG-DAN.txt`, rồi chạy dự án thử 2 giây trước. Bộ cài trên Windows/Mac cần Python **3.10+**. Mac có thể cần một dự án JSON chưa mã hóa trên chính máy người dùng để lấy thông tin nền tảng.

Để tạo lại từ nguồn:

```bash
node scripts/render-jianying-plate.mjs
.venv/bin/python scripts/export-jianying.py
.venv/bin/python scripts/validate-jianying.py
.venv/bin/python scripts/package-jianying.py
```

Kết quả: `out/MomBite01-Jianying.zip`. Mẫu bộ cài và adapter được lưu trong `jianying/`; nội dung, thời gian và âm thanh lấy từ `src/timeline.ts`. Video nền giữ ảnh, chuyển động máy quay, nhãn kênh và nhãn AI; tiêu đề, thông tin thực phẩm và lưu ý được chuyển thành chữ native.

Cỡ chữ, vị trí, nền chữ và hiệu ứng mờ trong Jianying là bản gần đúng. Chưa xác minh mở/chỉnh/xuất trực tiếp trong ứng dụng Jianying Windows/Mac. Khi đổi thứ tự cảnh, chọn cả đoạn hình và chữ/âm tương ứng để kéo cùng nhau. Giữ caption đăng mạng xã hội khỏi che phần lưu ý an toàn phía dưới.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `src/` | Video, timeline và manifest cho công cụ chỉnh sửa ShotCraft |
| `public/` | Ảnh minh họa, font và âm thanh |
| `scripts/` | Dựng video, xuất/kiểm tra/đóng gói Jianying |
| `jianying/` | Bộ cài và adapter Windows/Mac, không chứa định danh thiết bị |
| `deliverables/` | Thành phẩm đã giao |
| `docs/` | Brief, thiết kế, giấy phép và bằng chứng kiểm tra |
| `out/` | Kết quả dựng cục bộ, được Git bỏ qua |

## Kiểm tra và nguồn tài nguyên

Đã kiểm tra TypeScript, 16 khung hình, metadata video, âm lượng, hình ảnh giống nhau giữa hai bản, và sáu khung import ShotCraft khớp từng pixel. Dự án Jianying đã qua kiểm tra cấu trúc, tham chiếu tài nguyên và cài đặt giả lập; xem [báo cáo video](docs/independent-review.md), [báo cáo Jianying](docs/jianying-review.txt) và [kiểm tra bộ cài](docs/jianying-validation.txt).

Ảnh AI được tạo cho dự án này. Nhạc piano và âm chuyển cảnh được tổng hợp từ `scripts/make-audio.py`. Font Noto Sans có [giấy phép riêng](docs/OFL-NotoSans.txt); motion/adapter từ video-shotcraft có [giấy phép MIT](docs/video-shotcraft-LICENSE). Xem [nguồn và giới hạn](docs/provenance.md).

Thông tin dinh dưỡng bám theo brief người dùng; không hứa hẹn tăng IQ và không thay thế tư vấn chăm sóc thai kỳ. Các nguồn y khoa nêu trong brief chưa được kiểm chứng trực tuyến trong phiên dựng này.
