/* ==================================================================
   English / Vietnamese switch.

   The English text lives in index.html. Each translatable element
   carries data-i18n="key"; this file holds the Vietnamese for those
   keys. On first switch the English HTML of every tagged element is
   remembered, so switching back restores it exactly. Paper titles,
   venues and proper names stay in English.

   Other scripts read window.I18N.lang and listen for "langchange".
   ================================================================== */

(function () {
  "use strict";

  const VI = {
    "skip": "Bỏ qua, đến nội dung",
    "nav.research": "Nghiên cứu",
    "nav.work": "Dự án",
    "nav.pubs": "Công bố",
    "nav.edu": "Học vấn",
    "nav.contact": "Liên hệ",

    "hero.lede": "Tôi xây dựng AI tích hợp vật lý, đáng tin cậy cho kỹ thuật và khoa học: các mô hình học hệ động lực, giải phương trình đạo hàm riêng, thiết kế vật liệu, nhận dạng và điều khiển robot, cùng các tác tử LLM tự vận hành vòng lặp khám phá khoa học.",
    "hero.now": "Hiện tại",
    "hero.now1": "Nghiên cứu viên, VinUniversity — học máy và điều khiển cho robot",
    "hero.now2": "Trưởng nhóm kỹ thuật, VMV Technologies — AI, phần mềm và robot",
    "hero.phd": "Tiến sĩ",
    "hero.phd1": "Kỹ thuật Xây dựng, Đại học Vanderbilt, 2025",
    "hero.beng": "Kỹ sư",
    "hero.beng1": "Cơ điện tử, Đại học Bách khoa Hà Nội, 2019",

    "research.h2": "Hướng nghiên cứu",
    "research.lede": "Tám hướng, một mục tiêu: AI mà kỹ sư và nhà khoa học có thể tin cậy — vật lý được đưa vào mô hình, độ bất định đi kèm mọi câu trả lời, và các tác tử tự đảm nhận công việc, ứng dụng cho robot, vật liệu, camera và những công trình cần được giữ vững.",
    "ri.1.t": "Học máy tích hợp vật lý",
    "ri.1.d": "Đưa phương trình chủ đạo vào hàm mất mát. Mạng nơ-ron tích hợp vật lý và toán tử nơ-ron cho phương trình đạo hàm riêng có gián đoạn, nhiều miền và cấu trúc đa tỉ lệ.",
    "ri.2.t": "Định lượng bất định",
    "ri.2.d": "Quá trình Gauss phương sai thay đổi và mô hình tổ hợp cho những bài toán mà chính độ nhiễu cũng thay đổi theo đầu vào, chứ không chỉ riêng giá trị dự đoán.",
    "ri.3.t": "Mô hình ngôn ngữ lớn",
    "ri.3.d": "Mô hình Transformer và quy trình truy xuất tăng cường cho tài liệu và dữ liệu kỹ thuật, nơi một câu trả lời chỉ có giá trị khi kiểm chứng được với nguồn.",
    "ri.4.t": "AI tác tử cho khoa học",
    "ri.4.d": "Những hệ thống tự vận hành vòng lặp của mình — đề xuất không gian giả thuyết cho bài toán khám phá hệ thống thưa, kiểm tra rồi điều chỉnh, thay vì chờ được giao sẵn.",
    "ri.5.t": "Thị giác máy tính",
    "ri.5.d": "Đọc ảnh và video như một phép đo: ảnh vi cấu trúc dự đoán tính chất vật liệu, và hệ thống camera trả về con số thay vì nhãn.",
    "ri.6.t": "Học và điều khiển robot",
    "ri.6.d": "Động học ngược cho tay máy dư bậc tự do dưới dạng dự đoán tập hợp, hồi quy thưa cho động lực học hệ nhiều vật, và điều khiển kháng nhiễu cho tay máy phi tuyến.",
    "ri.7.t": "Khoa học vật liệu",
    "ri.7.d": "Ứng xử phi tuyến của tấm và vỏ nanocomposite, cùng thiết kế dựa trên dữ liệu, tìm kiếm trong không gian thành phần thay vì thử lần lượt.",
    "ri.8.t": "Giám sát sức khỏe kết cấu",
    "ri.8.d": "Đọc dấu hiệu dao động như một phép chẩn đoán: dạng dao động thay đổi cho biết hư hỏng nằm ở đâu và đã phát triển đến mức nào.",

    "work.h2": "Dự án ứng dụng",
    "work.lede": "Nơi nghiên cứu rời trang giấy: những hệ thống phải chạy tại cơ sở của người khác, trên phần cứng của họ, với dữ liệu của họ.",
    "vcv.meta": "Trưởng nhóm kỹ thuật · <a href=\"https://vcv-cam.onrender.com/\">vcv-cam.onrender.com</a>",
    "vcv.sum": "Phân tích video bằng AI, biến các camera IP sẵn có thành hệ thống giám sát mà không phải thay phần cứng.",
    "vcv.k1": "Đầu vào", "vcv.v1": "Camera IP sẵn có qua RTSP hoặc ONVIF",
    "vcv.k2": "Xử lý", "vcv.v2": "Phát hiện theo quy tắc, chạy tại chỗ",
    "vcv.k3": "Cài đặt", "vcv.v3": "Tự vẽ vùng trên khung hình, không cần code",
    "vcv.k4": "Đầu ra", "vcv.v4": "Cảnh báo kèm ảnh và thời gian qua web, app, Zalo",
    "vcv.k5": "Phạm vi", "vcv.v5": "12 lĩnh vực, 36 giải pháp, từ phòng cháy đến OCR",
    "vmv.meta": "Trưởng nhóm kỹ thuật · <a href=\"https://vmvtechnologies.com/vi\">vmvtechnologies.com</a>",
    "vmv.sum": "AI, phần mềm và robot cho doanh nghiệp Việt Nam, xây trên chính dữ liệu và quy trình của họ, để khách hàng sở hữu hệ thống thay vì đi thuê.",
    "vmv.v1": "Tư vấn, phát triển và tích hợp trên dữ liệu khách hàng",
    "vmv.k2": "Phần mềm", "vmv.v2": "Web, app và dashboard nối vào hệ thống sẵn có",
    "vmv.k3": "Robot", "vmv.v3": "Tự động hóa dây chuyền, đến khâu tích hợp",
    "vmv.k4": "Bàn giao", "vmv.v4": "Chuyển giao mã nguồn và kiến thức cho khách hàng",
    "vmv.k5": "Đã làm", "vmv.v5": "Trợ lý có trích nguồn và phiên dịch trực tiếp",

    "tool.h2": "Công cụ",
    "tool.lede": "Những gì thực sự được dùng để làm ra các công việc trên.",
    "tool.k1": "Framework học máy",
    "tool.k2": "Phương pháp học",
    "tool.v2": "Mạng nơ-ron tích hợp vật lý, toán tử nơ-ron, CNN, quá trình Gauss, tối ưu Bayes, định lượng bất định",
    "tool.k3": "Tính toán khoa học",
    "tool.v3": "Python, C/C++, MATLAB, NumPy, SciPy, Pandas, Git, Linux, Docker, tính toán hiệu năng cao",
    "tool.k4": "Kỹ thuật tính toán",
    "tool.v4": "FEniCS, phương pháp phần tử hữu hạn, SALOME, Abaqus, COMSOL, SolidWorks",
    "tool.k5": "Robot và điều khiển",
    "tool.v5": "Động học ngược, nhận dạng động lực học, hồi quy thưa, học tăng cường, điều khiển dự báo mô hình phi tuyến",
    "tool.k6": "Tác tử và truy xuất",
    "tool.v6": "LangChain, CrewAI, sinh tăng cường truy xuất (RAG), cơ sở dữ liệu vector, điều phối đa tác tử",

    "pubs.h2": "Công bố",
    "pubs.lede1": "Các công trình đã xuất bản và được chấp nhận, mới nhất trước.",
    "pubs.lede2": "Dấu sao đánh dấu đồng tác giả chính.",
    "pubs.chart": "Số công bố mỗi năm",
    "pubs.journal": "Bài báo tạp chí",
    "pubs.conf": "Bài báo hội nghị",
    "pubs.none": "Không có công bố nào trong hướng này.",

    "edu.h2": "Học vấn",
    "edu.lede": "Nền tảng đào tạo.",
    "edu.r1": "Tiến sĩ, Kỹ thuật Xây dựng",
    "edu.r1b": "Đại học Vanderbilt<span class=\"role\">Hướng dẫn: Ravindra Duddu, Abhinav Gupta</span>",
    "edu.r2": "Thạc sĩ, Kỹ thuật Xây dựng",
    "edu.r2b": "Đại học Vanderbilt<span class=\"role\">Hướng dẫn: Ravindra Duddu</span>",
    "edu.r3": "Kỹ sư, Cơ điện tử",
    "edu.r3b": "Đại học Bách khoa Hà Nội<span class=\"role\">Hướng dẫn: TS. Đinh Gia Ninh</span>",
    "teach.h2": "Giảng dạy",
    "teach.lede": "Các môn trợ giảng song song với nghiên cứu.",
    "teach.r1": "Cơ điện tử",
    "teach.r1b": "VinUniversity<span class=\"role\">Trợ giảng</span>",
    "teach.r1w": "2026 — nay",
    "teach.r2": "Sức bền vật liệu",
    "teach.r2b": "Đại học Vanderbilt<span class=\"role\">Trợ giảng sau đại học</span>",
    "teach.r3": "Tĩnh học",
    "teach.r3b": "Đại học Vanderbilt<span class=\"role\">Trợ giảng sau đại học, tổng cộng tám học kỳ</span>",

    "contact.h2": "Liên hệ",
    "contact.alumni": "Cựu học viên",
    "contact.based": "Nơi ở",
    "contact.city": "Hà Nội, Việt Nam",
    "contact.qr": "Zalo — quét mã để nhắn tin",

    "foot.note": "Trang tĩnh, không theo dõi. Mã nguồn trên <a href=\"https://github.com/Tiennd11\">GitHub</a>."
  };

  const UI = {
    en: { menu: "Menu", close: "Close", all: "All work",
          count: (n, j, c) => n + " entries — " + j + " journal articles and " + c + " conference papers." },
    vi: { menu: "Mục lục", close: "Đóng", all: "Tất cả",
          count: (n, j, c) => n + " công bố — " + j + " bài tạp chí và " + c + " bài hội nghị." }
  };

  const THREADS_VI = {
    sciml: "Học máy khoa học", robotics: "Robot", fracture: "Phá hủy",
    structdyn: "Động lực học kết cấu", uq: "Bất định", agentic: "AI tác tử"
  };

  const KEY = "site-lang";
  const store = {
    get: function () { try { return localStorage.getItem(KEY); } catch (e) { return null; } },
    set: function (v) { try { localStorage.setItem(KEY, v); } catch (e) { /* private mode */ } }
  };

  const nodes = Array.prototype.slice.call(document.querySelectorAll("[data-i18n]"));
  nodes.forEach(function (el) { el.dataset.en = el.innerHTML; });

  const I18N = {
    lang: "en",
    ui: function (k) { return UI[I18N.lang][k]; },
    thread: function (key, english) { return I18N.lang === "vi" ? (THREADS_VI[key] || english) : english; },
    set: function (lang) {
      if (lang !== "vi") lang = "en";
      I18N.lang = lang;
      nodes.forEach(function (el) {
        const k = el.getAttribute("data-i18n");
        el.innerHTML = lang === "vi" && VI[k] ? VI[k] : el.dataset.en;
      });
      document.documentElement.lang = lang;
      Array.prototype.forEach.call(document.querySelectorAll(".lang button"), function (b) {
        b.setAttribute("aria-pressed", String(b.dataset.lang === lang));
      });
      store.set(lang);
      document.dispatchEvent(new CustomEvent("langchange", { detail: { lang: lang } }));
    }
  };
  window.I18N = I18N;

  Array.prototype.forEach.call(document.querySelectorAll(".lang button"), function (b) {
    b.addEventListener("click", function () { I18N.set(b.dataset.lang); });
  });

  const saved = store.get();
  if (saved === "vi") I18N.set("vi");
})();
