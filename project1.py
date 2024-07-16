#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, simpledialog
import psycopg2

def submit():
    tk.Label(root, text="Name:").pack()
    name = tk.Entry(root)
    name.pack()
    tk.Label(root, text="price:").pack()
    price= tk.Entry(root)
    price.pack()
    tk.Label(root, text="Quantity:").pack()
    quanty = tk.Entry(root)
    quanty.pack()
    tk.Label(root, text="ID:").pack()
    idd= tk.Entry(root)
    idd.pack()
    
    
    if name and price and quanty and idd:
        try:
            conn = psycopg2.connect(dbname="22105056",
                user="postgres",
                password="sri5319",
                host="localhost",  
                port="5432")
            cur = conn.cursor()
            cur.execute("INSERT INTO products (id, name, price, quantity) VALUES (%s, %s, %s, %s)", (idd, name, price, quanty))
            conn.commit()
            messagebox.showinfo("Success!", "Data saved successfully")
        except psycopg2.Error as e:
            conn.rollback()
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn:
                cur.close()
                conn.close()
    else:
        messagebox.showerror("Input Error", "All fields are required.")

def update():
    idd = simpledialog.askinteger("Update Data", "Enter product ID to update:")
    if idd:
        try:
            conn = psycopg2.connect(dbname="22105056",
                user="postgres",
                password="sri5319",
                host="localhost",  
                port="5432")
            cur = conn.cursor()
            cur.execute("SELECT * FROM products WHERE id = %s", (idd,))
            row = cur.fetchone()
            if row:
                name = simpledialog.askstring("Update Data", "Enter new product name:", initialvalue=row[1])
                price = simpledialog.askfloat("Update Data", "Enter new product price:", initialvalue=row[2])
                quanty = simpledialog.askinteger("Update Data", "Enter new product quantity:", initialvalue=row[3])
                if name and price and quanty:
                    cur.execute("UPDATE products SET name=%s, price=%s, quantity=%s WHERE id=%s", (name, price, quanty, idd))
                    conn.commit()
                    messagebox.showinfo("Success!", "Data updated successfully")
                else:
                    messagebox.showerror("Input Error", "All fields are required.")
            else:
                messagebox.showerror("Error!", f"No product found with ID {idd}")
        except psycopg2.Error as e:
            conn.rollback()
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn:
                cur.close()
                conn.close()
    else:
        messagebox.showerror("Input Error", "Product ID is required.")

def retrieve_products():
    try:
        conn = psycopg2.connect(dbname="22105056",
            user="postgres",
            password="sri5319",
            host="localhost",  
            port="5432")
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn:
            cur.close()
            conn.close()

def delete():
    idd = simpledialog.askinteger("Delete Data", "Enter product ID to delete:")
    if idd:
        try:
            conn = psycopg2.connect(dbname="22105056",
                user="postgres",
                password="sri5319",
                host="localhost",  
                port="5432")
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE id = %s", (idd,))
            conn.commit()
            messagebox.showinfo("Success!", "Data deleted successfully")
        except psycopg2.Error as e:
            conn.rollback()
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn:
                cur.close()
                conn.close()
    else:
        messagebox.showerror("Input Error", "Product ID is required.")

def show_menu():
    choice = simpledialog.askstring("Menu", "Select an option:\n1. Insert\n2. Retrieve\n3. Update\n4. Delete")
    if choice == "1":
        submit()
    elif choice == "2":
        retrieve_products()
    elif choice == "3":
        update()
    elif choice == "4":
        delete()
    else:
        messagebox.showerror("Error", "Invalid choice")

root = tk.Tk()
root.title("Sales Data")

menu_button = tk.Button(root, text="Show Menu", command=show_menu)
menu_button.pack()

root.mainloop()
