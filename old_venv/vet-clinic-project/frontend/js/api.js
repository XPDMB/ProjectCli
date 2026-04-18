/**
 * เรียก REST API ของคลินิก
 */
(function (global) {
  // Determine API Base URL
  // If we are on port 8000 (Django serving frontend), use current origin.
  // Otherwise, fallback to 127.0.0.1:8000 (Django dev server).
  // หากเรารันผ่าน ngrok หรือ domain อื่นๆ ให้ใช้ origin นั้นๆ เป็น base API ทันที
  const isLocalhost = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
  const isDefaultDevPort = window.location.port === "8000";
  
  const API_BASE = (isDefaultDevPort || !isLocalhost)
    ? `${window.location.origin}/api/v1`
    : "http://127.0.0.1:8000/api/v1";

  // API Base URL determined automatically

  function authHeaders(extra) {
    const h = { "Content-Type": "application/json", ...(extra || {}) };
    const t = localStorage.getItem("token");
    if (t) h.Authorization = "Token " + t;
    return h;
  }

  async function apiFetch(path, options) {
    options = options || {};
    const res = await fetch(API_BASE + path, {
      ...options,
      headers: authHeaders(options.headers),
    });
    const text = await res.text();
    var data = null;
    try {
      data = text ? JSON.parse(text) : null;
    } catch (e) {
      data = { detail: text };
    }
    if (!res.ok) {
      let msg = "เกิดข้อผิดพลาดในการเชื่อมต่อ";
      if (data) {
        if (typeof data === "string") {
          msg = data;
        } else if (data.detail) {
          msg = data.detail;
        } else if (typeof data === "object") {
          // Collect all field errors: { "email": ["error"], "phone": ["error"] }
          const errors = [];
          for (const key in data) {
            const val = data[key];
            const displayKey = key === "email" ? "อีเมล" : key === "phone" ? "เบอร์โทร" : key;
            if (Array.isArray(val)) {
              errors.push(`${displayKey}: ${val[0]}`);
            } else {
              errors.push(`${displayKey}: ${val}`);
            }
          }
          if (errors.length > 0) msg = errors.join(", ");
        }
      }
      var err = new Error(msg);
      err.status = res.status;
      err.data = data;
      throw err;
    }

    // แจ้งเตือนเมื่อบันทึกลง SQL สำเร็จ (เฉพาะ POST, PUT, DELETE)
    const method = (options.method || "GET").toUpperCase();
    if (["POST", "PUT", "DELETE", "PATCH"].includes(method)) {
      if (window.VetUi && window.VetUi.showSqlSuccess) {
        window.VetUi.showSqlSuccess();
      }
    }

    return data;
  }

  global.VetApi = {
    apiFetch: apiFetch,
    BASE_URL: API_BASE,

    registerUser: function (payload) {
      return apiFetch("/auth/register/", {
        method: "POST",
        body: JSON.stringify(payload),
      }).then(function (data) {
        if (data.token) localStorage.setItem("token", data.token);
        return data;
      });
    },

    loginUser: function (payload) {
      return apiFetch("/login/", {
        method: "POST",
        body: JSON.stringify(payload),
      }).then(function (data) {
        if (data.token) localStorage.setItem("token", data.token);
        return data;
      });
    },

    logoutUser: function () {
      localStorage.removeItem("token");
    },

    fetchMe: function () {
      return apiFetch("/me/");
    },

    fetchPets: function () {
      return apiFetch("/pets/");
    },

    fetchStaff: function () {
      return apiFetch("/staff/");
    },

    createPet: function (body) {
      return apiFetch("/pets/", { method: "POST", body: JSON.stringify(body) });
    },

    bookAppointment: function (payload) {
      return apiFetch("/book-appointment/", {
        method: "POST",
        body: JSON.stringify(payload),
      });
    },

    fetchAppointments: function (params) {
      var q = params ? "?" + params : "";
      return apiFetch("/appointments/" + q);
    },

    confirmAppointment: function (id) {
      return apiFetch("/appointments/" + id + "/confirm/", {
        method: "POST",
        body: "{}",
      });
    },

    cancelAppointment: function (id) {
      return apiFetch("/appointments/" + id + "/cancel/", {
        method: "POST",
        body: "{}",
      });
    },

    deleteAppointment: function (id) {
      return apiFetch("/appointments/" + id + "/", {
        method: "DELETE",
      });
    },

    fetchInventory: function () {
      return apiFetch("/inventory/");
    },

    createInventory: function (body) {
      return apiFetch("/inventory/", {
        method: "POST",
        body: JSON.stringify(body),
      });
    },

    updateInventory: function (id, body) {
      return apiFetch("/inventory/" + id + "/", {
        method: "PATCH", // Use PATCH for partial updates
        body: JSON.stringify(body),
      });
    },

    deleteInventory: function (id) {
      return apiFetch("/inventory/" + id + "/", {
        method: "DELETE",
      });
    },

    fetchMedicalRecords: function (params) {
      var q = params ? "?" + params : "";
      return apiFetch("/medical-records/" + q);
    },

    createMedicalRecord: function (body) {
      return apiFetch("/medical-records/", {
        method: "POST",
        body: JSON.stringify(body),
      });
    },

    payMedicalRecord: function (id) {
      return apiFetch(`/medical-records/${id}/pay/`, {
        method: "POST"
      });
    },

    fetchFinancialReport: function (days) {
      return apiFetch(`/report/financial/?days=${days || 7}`);
    },

    fetchStaffShifts: function () {
      return apiFetch("/staff-shifts/");
    },

    createStaffShift: function (body) {
      return apiFetch("/staff-shifts/", {
        method: "POST",
        body: JSON.stringify(body),
      });
    },
  };
})(typeof window !== "undefined" ? window : this);
