/** ฟังก์ชันช่วยแสดงข้อความผิดพลาด */
function showErr(el, err) {
  if (!el) return;
  el.style.display = "block";
  el.textContent = err.message || String(err);
}

function hideErr(el) {
  if (!el) return;
  el.style.display = "none";
  el.textContent = "";
}

function badgeClass(status) {
  if (status === "confirmed") return "badge-ok";
  if (status === "cancelled") return "badge-cancel";
  return "badge-pending";
}

function badgeText(status) {
  if (status === "confirmed") return "ยืนยันแล้ว";
  if (status === "cancelled") return "ยกเลิก";
  return "รอยืนยัน";
}

function showSqlSuccess() {
  const toast = document.createElement("div");
  toast.className = "sql-toast animate-gentle";
  toast.innerHTML = `
    <div style="display:flex; align-items:center; gap:12px;">
      <div style="background:#06C755; color:white; width:28px; height:28px; border-radius:50%; display:flex; padding-left:7px; align-items:center; justify-center; font-size:14px;">
        <i class="fas fa-check"></i>
      </div>
      <div>
        <div style="font-weight:900; font-size:13px; color:#064E3B;">SUCCESS</div>
        <div style="font-size:12px; color:#065F46; font-weight:bold;">บันทึกข้อมูลลง SQL Server เรียบร้อยแล้ว</div>
      </div>
    </div>
  `;
  
  // Basic CSS for the toast
  Object.assign(toast.style, {
    position: "fixed",
    bottom: "30px",
    right: "30px",
    background: "white",
    padding: "16px 24px",
    borderRadius: "20px",
    boxShadow: "0 20px 40px rgba(6, 199, 85, 0.2)",
    border: "2px solid #06C755",
    zIndex: "9999",
    cursor: "pointer",
    minWidth: "280px"
  });

  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(20px)";
    toast.style.transition = "all 0.5s ease";
    setTimeout(() => toast.remove(), 500);
  }, 3000);
}

window.VetUi = { showErr: showErr, hideErr: hideErr, badgeClass: badgeClass, badgeText: badgeText, showSqlSuccess: showSqlSuccess };
