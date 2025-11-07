import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import mysql.connector

# --- Backend Functions ---
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ruthu2006@",  # Replace with your MySQL password
        database="farmer_db"
    )

def save_farmer(vals):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO farmers
          (name, crop_type, location, phone, farm_size, soil_type, irrigation)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, vals)
    conn.commit()
    conn.close()

def update_farmer_db(vals, fid):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE farmers SET
          name=%s, crop_type=%s, location=%s, phone=%s,
          farm_size=%s, soil_type=%s, irrigation=%s
        WHERE id=%s
    """, (*vals, fid))
    conn.commit()
    conn.close()

def delete_farmer_db(fid):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM farmers WHERE id=%s", (fid,))
    conn.commit()
    conn.close()

def search_farmer_by_id(fid):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM farmers WHERE id=%s", (fid,))
    rec = cur.fetchone()
    conn.close()
    return rec

def search_farmer_by_name(name):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM farmers WHERE name LIKE %s", ('%' + name + '%',))
    recs = cur.fetchall()
    conn.close()
    return recs

# --- GUI Setup ---
root = tk.Tk()
root.title("Farmers Management System")
root.attributes('-fullscreen', True)  # Fullscreen

# Load and set background for main page
def set_background(win, img_path):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    bg = Image.open(img_path).resize((screen_w, screen_h), Image.Resampling.LANCZOS)
    bg_img = ImageTk.PhotoImage(bg)
    canvas = tk.Canvas(win, width=screen_w, height=screen_h, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_img)
    # keep a reference to prevent GC
    win.bg_img = bg_img
    return canvas

# Main page: navigation buttons
canvas_main = set_background(root, "logo.jpg")

btn_add = tk.Button(root, text="Add Farmer", font=("Arial",14,"bold"), bg="#28a745", fg="white", command=lambda: open_add_page())
btn_update = tk.Button(root, text="Update Farmer", font=("Arial",14,"bold"), bg="#007bff", fg="white", command=lambda: open_update_page())
btn_search = tk.Button(root, text="Search Farmer", font=("Arial",14,"bold"), bg="#17a2b8", fg="white", command=lambda: open_search_page())
btn_delete = tk.Button(root, text="Delete Farmer", font=("Arial",14,"bold"), bg="#dc3545", fg="white", command=lambda: open_delete_page())
btn_exit = tk.Button(root, text="Exit", font=("Arial",14,"bold"), bg="#6c757d", fg="white", command=root.destroy)

# place buttons on canvas
canvas_main.create_window(450, 250, window=btn_add, width=200, height=50)
canvas_main.create_window(450, 320, window=btn_update, width=200, height=50)
canvas_main.create_window(450, 390, window=btn_search, width=200, height=50)
canvas_main.create_window(450, 460, window=btn_delete, width=200, height=50)
canvas_main.create_window(450, 530, window=btn_exit, width=200, height=50)

# --- Add Farmer Page ---
def open_add_page():
    page = tk.Toplevel(root)
    page.title("Add Farmer")
    page.geometry("900x600")
    canvas = set_background(page, "crop_image.jpg")

    # form frame
    frm = tk.Frame(page, bg="#ffffff", padx=10, pady=10)
    canvas.create_window(450, 300, window=frm)

    labels = ["Name","Crop Type","Location","Phone","Farm Size","Soil Type","Irrigation"]
    entries = {}
    for i, txt in enumerate(labels):
        tk.Label(frm, text=txt, bg="#fff").grid(row=i, column=0, sticky="e", pady=5, padx=5)
        e = tk.Entry(frm)
        e.grid(row=i, column=1, pady=5, padx=5)
        entries[txt] = e

    def on_save():
        vals = tuple(entries[k].get().strip() for k in labels)
        if any(not v for v in vals):
            messagebox.showerror("Input Error","All fields are required.")
            return
        try:
            save_farmer(vals)
            messagebox.showinfo("Success","Farmer added.")
            page.destroy()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    btn = tk.Button(frm, text="Save Farmer", font=("Arial",12,"bold"), bg="#28a745", fg="white", command=on_save)
    btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

# --- Update Farmer Page ---
def open_update_page():
    fid = simpledialog.askinteger("Update Farmer","Enter Farmer ID to update:")
    if fid is None:
        return
    rec = search_farmer_by_id(fid)
    if not rec:
        messagebox.showerror("Not Found","No farmer with that ID.")
        return

    page = tk.Toplevel(root)
    page.title("Update Farmer")
    page.geometry("900x600")
    canvas = set_background(page, "crop_image.jpg")

    frm = tk.Frame(page, bg="#ffffff", padx=10, pady=10)
    canvas.create_window(450, 300, window=frm)

    labels = ["Name","Crop Type","Location","Phone","Farm Size","Soil Type","Irrigation"]
    entries = []
    for i, txt in enumerate(labels):
        tk.Label(frm, text=txt, bg="#fff").grid(row=i, column=0, sticky="e", pady=5, padx=5)
        e = tk.Entry(frm)
        e.grid(row=i, column=1, pady=5, padx=5)
        e.insert(0, rec[i+1])
        entries.append(e)

    def on_update():
        vals = [e.get().strip() for e in entries]
        if any(not v for v in vals):
            messagebox.showerror("Input Error","All fields required.")
            return
        try:
            update_farmer_db(vals, fid)
            messagebox.showinfo("Success","Farmer updated.")
            page.destroy()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    btn = tk.Button(frm, text="Update Farmer", font=("Arial",12,"bold"), bg="#ffc107", fg="black", command=on_update)
    btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

# --- Search Farmer Page --- 
def open_search_page():
    page = tk.Toplevel(root)
    page.title("Search Farmer")
    page.geometry("900x600")
    canvas = set_background(page, "search_bg.jpg")

    frm = tk.Frame(page, bg="#ffffff", padx=10, pady=10)
    canvas.create_window(450, 100, window=frm)

    tk.Label(frm, text="Farmer Name:", bg="#fff").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(frm)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    def perform_search():
        name = name_entry.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Please enter a Farmer Name.")
            return

        records = search_farmer_by_name(name)

        if not records:
            messagebox.showinfo("No Results", "No matching records found.")
            return

        # Display results in Treeview
        result_frame = tk.Frame(page)
        canvas.create_window(450, 350, window=result_frame)
        cols = ("ID", "Name", "Crop Type", "Location", "Phone", "Farm Size", "Soil Type", "Irrigation")
        tree = ttk.Treeview(result_frame, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for rec in records:
            tree.insert("", "end", values=rec)
        tree.pack()

    btn_search = tk.Button(frm, text="Search", font=("Arial",12,"bold"), bg="#17a2b8", fg="white", command=perform_search)
    btn_search.grid(row=1, column=0, columnspan=2, pady=10)

# --- Delete Farmer Page ---
def open_delete_page():
    fid = simpledialog.askinteger("Delete Farmer","Enter Farmer ID to delete:")
    if fid is None:
        return
    rec = search_farmer_by_id(fid)
    if not rec:
        messagebox.showerror("Not Found","No farmer with that ID.")
        return
    confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this record?")
    if confirm:
        # Proceed with deletion
        delete_farmer_db(fid)  # Corrected the indentation here
        messagebox.showinfo("Success", "Farmer deleted.")
    else:
        # Cancellation logic
        pass

root.mainloop()
